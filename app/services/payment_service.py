"""Payment management service.

Handles recording payments against invoices. Payments reduce
the outstanding balance on an invoice and affect the school/student
account statements.
"""
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.cache import cache_invalidate_prefix
from app.core.exceptions import BusinessRuleError, EntityNotFoundError, ValidationError
from app.models.invoice import Invoice, InvoiceStatus
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate
from app.utils.pagination import paginate


def get_payment(db: Session, payment_id: int) -> Payment | None:
    return db.get(Payment, payment_id)


def list_payments(
    db: Session,
    limit: int,
    offset: int,
    invoice_id: int | None = None,
    student_id: int | None = None,
    school_id: int | None = None,
) -> dict:
    base_query = select(Payment)

    if invoice_id is not None or student_id is not None or school_id is not None:
        base_query = base_query.join(Invoice)

    if invoice_id is not None:
        base_query = base_query.where(Payment.invoice_id == invoice_id)

    if student_id is not None:
        base_query = base_query.where(Invoice.student_id == student_id)

    if school_id is not None:
        base_query = base_query.where(Invoice.school_id == school_id)

    return paginate(base_query, db, limit, offset)


def create_payment(db: Session, payment_in: PaymentCreate) -> Payment:
    """Record a payment against an invoice.
    
    Business Rules:
    - Invoice must exist and not be cancelled
    - Payment amount must be positive
    - Total payments cannot exceed invoice amount (no overpayment)
    
    Side Effects:
    - Invalidates cached statements for the related school and student
    """
    invoice = db.get(Invoice, payment_in.invoice_id)
    if not invoice:
        raise EntityNotFoundError("Invoice", payment_in.invoice_id)
    if invoice.status == InvoiceStatus.cancelled:
        raise BusinessRuleError("Cannot add payment to cancelled invoice")
    if payment_in.amount <= 0:
        raise ValidationError("Payment amount must be greater than zero")

    # Prevent overpayment
    total_paid = sum((p.amount for p in invoice.payments or []), Decimal("0"))
    if total_paid + payment_in.amount > invoice.amount:
        raise BusinessRuleError("Total payments cannot exceed invoice amount")

    payment = Payment(**payment_in.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    cache_invalidate_prefix(
        f"cache:GET:/api/v1/schools/{invoice.school_id}/statement"
    )
    cache_invalidate_prefix(
        f"cache:GET:/api/v1/students/{invoice.student_id}/statement"
    )
    return payment
