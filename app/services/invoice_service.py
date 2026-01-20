"""Invoice management service.

Handles creation, updates, and cancellation of invoices.
Invoices are financial records linking a student to a school
with an amount due by a specific date.
"""
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.cache import cache_invalidate_prefix
from app.core.exceptions import EntityNotFoundError, ValidationError
from app.models.invoice import Invoice, InvoiceStatus
from app.models.student import Student
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate
from app.utils.pagination import paginate


def get_invoice(db: Session, invoice_id: int) -> Invoice | None:
	return db.get(Invoice, invoice_id)


def _validate_invoice_input(
	db: Session,
	*,
	school_id: int,
	student_id: int,
	issue_date: date,
	due_date: date,
	amount: float,
) -> None:
	"""Validate invoice data before creation or update.
	
	Business Rules:
	- Student must exist and belong to the specified school
	- Amount must be positive
	- Due date must be on or after issue date
	"""
	student = db.get(Student, student_id)
	if not student:
		raise EntityNotFoundError("Student", student_id)
	if student.school_id != school_id:
		raise ValidationError("Invoice school_id must match student's school_id")
	if amount <= 0:
		raise ValidationError("Invoice amount must be greater than zero")
	if due_date < issue_date:
		raise ValidationError("Invoice due_date must be on or after issue_date")


def list_invoices(
	db: Session,
	limit: int,
	offset: int,
	school_id: int | None = None,
	student_id: int | None = None,
	status: InvoiceStatus | None = None,
) -> dict:
	base_query = select(Invoice)

	if school_id is not None:
		base_query = base_query.where(Invoice.school_id == school_id)

	if student_id is not None:
		base_query = base_query.where(Invoice.student_id == student_id)

	if status is not None:
		base_query = base_query.where(Invoice.status == status)

	return paginate(base_query, db, limit, offset)


def create_invoice(db: Session, invoice_in: InvoiceCreate) -> Invoice:
	_validate_invoice_input(
		db,
		school_id=invoice_in.school_id,
		student_id=invoice_in.student_id,
		issue_date=invoice_in.issue_date,
		due_date=invoice_in.due_date,
		amount=float(invoice_in.amount),
	)
	invoice = Invoice(**invoice_in.model_dump())
	db.add(invoice)
	db.commit()
	db.refresh(invoice)
	cache_invalidate_prefix(
		f"cache:GET:/api/v1/schools/{invoice.school_id}/statement"
	)
	cache_invalidate_prefix(
		f"cache:GET:/api/v1/students/{invoice.student_id}/statement"
	)
	return invoice


def update_invoice(db: Session, invoice_id: int, invoice_in: InvoiceUpdate) -> Invoice | None:
	invoice = db.get(Invoice, invoice_id)
	if not invoice:
		return None
	updates = invoice_in.model_dump(exclude_unset=True)
	school_id = updates.get("school_id", invoice.school_id)
	student_id = updates.get("student_id", invoice.student_id)
	issue_date = updates.get("issue_date", invoice.issue_date)
	due_date = updates.get("due_date", invoice.due_date)
	amount = float(updates.get("amount", invoice.amount))

	_validate_invoice_input(
		db,
		school_id=school_id,
		student_id=student_id,
		issue_date=issue_date,
		due_date=due_date,
		amount=amount,
	)

	for field, value in updates.items():
		setattr(invoice, field, value)
	db.commit()
	db.refresh(invoice)
	cache_invalidate_prefix(
		f"cache:GET:/api/v1/schools/{invoice.school_id}/statement"
	)
	cache_invalidate_prefix(
		f"cache:GET:/api/v1/students/{invoice.student_id}/statement"
	)
	return invoice


def cancel_invoice(db: Session, invoice_id: int) -> Invoice | None:
	"""Cancel an invoice.
	
	Note: In production, should validate that no payments exist
	or require refunding payments before cancellation.
	"""
	invoice = db.get(Invoice, invoice_id)
	if not invoice:
		return None
	invoice.status = InvoiceStatus.cancelled
	db.commit()
	db.refresh(invoice)
	cache_invalidate_prefix(
		f"cache:GET:/api/v1/schools/{invoice.school_id}/statement"
	)
	cache_invalidate_prefix(
		f"cache:GET:/api/v1/students/{invoice.student_id}/statement"
	)
	return invoice
