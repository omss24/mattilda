import pytest

from app.core.exceptions import BusinessRuleError, EntityNotFoundError, ValidationError
from app.models.invoice import InvoiceStatus
from app.schemas.invoice import InvoiceCreate
from app.schemas.payment import PaymentCreate
from app.schemas.school import SchoolCreate
from app.schemas.student import StudentCreate
from app.services.invoice_service import cancel_invoice, create_invoice
from app.services.payment_service import create_payment
from app.services.school_service import create_school
from app.services.student_service import create_student


def _create_invoice(db_session):
    school = create_school(db_session, SchoolCreate(name="Payment School"))
    student = create_student(
        db_session,
        StudentCreate(
            school_id=school.id,
            first_name="Mia",
            last_name="Torres",
        ),
    )
    invoice = create_invoice(
        db_session,
        InvoiceCreate(
            school_id=school.id,
            student_id=student.id,
            issue_date="2026-01-01",
            due_date="2026-01-10",
            amount="100.00",
            currency="MXN",
            status=InvoiceStatus.pending,
        ),
    )
    return invoice


def test_payment_requires_existing_invoice(db_session):
    payment_in = PaymentCreate(
        invoice_id=999,
        paid_at="2026-01-05T10:00:00",
        amount="10.00",
        method="transfer",
    )
    with pytest.raises(EntityNotFoundError, match="Invoice"):
        create_payment(db_session, payment_in)


def test_payment_amount_must_be_positive(db_session):
    invoice = _create_invoice(db_session)
    payment_in = PaymentCreate(
        invoice_id=invoice.id,
        paid_at="2026-01-05T10:00:00",
        amount="0",
        method="transfer",
    )
    with pytest.raises(ValidationError, match="amount must be greater than zero"):
        create_payment(db_session, payment_in)


def test_payment_cannot_target_cancelled_invoice(db_session):
    invoice = _create_invoice(db_session)
    cancel_invoice(db_session, invoice.id)
    payment_in = PaymentCreate(
        invoice_id=invoice.id,
        paid_at="2026-01-05T10:00:00",
        amount="10.00",
        method="transfer",
    )
    with pytest.raises(BusinessRuleError, match="cancelled invoice"):
        create_payment(db_session, payment_in)


def test_payment_total_cannot_exceed_invoice_amount(db_session):
    invoice = _create_invoice(db_session)
    create_payment(
        db_session,
        PaymentCreate(
            invoice_id=invoice.id,
            paid_at="2026-01-05T10:00:00",
            amount="80.00",
            method="transfer",
        ),
    )
    with pytest.raises(BusinessRuleError, match="cannot exceed"):
        create_payment(
            db_session,
            PaymentCreate(
                invoice_id=invoice.id,
                paid_at="2026-01-06T10:00:00",
                amount="30.00",
                method="transfer",
            ),
        )
