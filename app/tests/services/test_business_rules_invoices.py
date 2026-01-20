import pytest

from app.core.exceptions import EntityNotFoundError, ValidationError
from app.models.invoice import InvoiceStatus
from app.schemas.invoice import InvoiceCreate
from app.schemas.school import SchoolCreate
from app.schemas.student import StudentCreate
from app.services.invoice_service import create_invoice
from app.services.school_service import create_school
from app.services.student_service import create_student


def _create_school_and_student(db_session):
    school = create_school(db_session, SchoolCreate(name="Invoice School"))
    student = create_student(
        db_session,
        StudentCreate(
            school_id=school.id,
            first_name="Luis",
            last_name="Perez",
        ),
    )
    return school, student


def test_invoice_requires_existing_student(db_session):
    school = create_school(db_session, SchoolCreate(name="Invoice School"))
    invoice_in = InvoiceCreate(
        school_id=school.id,
        student_id=999,
        issue_date="2026-01-01",
        due_date="2026-01-10",
        amount="100.00",
        currency="MXN",
        status=InvoiceStatus.pending,
    )
    with pytest.raises(EntityNotFoundError, match="Student"):
        create_invoice(db_session, invoice_in)


def test_invoice_school_id_must_match_student(db_session):
    school, student = _create_school_and_student(db_session)
    other_school = create_school(db_session, SchoolCreate(name="Other School"))
    invoice_in = InvoiceCreate(
        school_id=other_school.id,
        student_id=student.id,
        issue_date="2026-01-01",
        due_date="2026-01-10",
        amount="100.00",
        currency="MXN",
        status=InvoiceStatus.pending,
    )
    with pytest.raises(ValidationError, match="school_id must match"):
        create_invoice(db_session, invoice_in)


def test_invoice_amount_must_be_positive(db_session):
    school, student = _create_school_and_student(db_session)
    invoice_in = InvoiceCreate(
        school_id=school.id,
        student_id=student.id,
        issue_date="2026-01-01",
        due_date="2026-01-10",
        amount="0",
        currency="MXN",
        status=InvoiceStatus.pending,
    )
    with pytest.raises(ValidationError, match="amount must be greater than zero"):
        create_invoice(db_session, invoice_in)


def test_invoice_due_date_must_be_after_issue_date(db_session):
    school, student = _create_school_and_student(db_session)
    invoice_in = InvoiceCreate(
        school_id=school.id,
        student_id=student.id,
        issue_date="2026-01-10",
        due_date="2026-01-01",
        amount="100.00",
        currency="MXN",
        status=InvoiceStatus.pending,
    )
    with pytest.raises(ValidationError, match="due_date"):
        create_invoice(db_session, invoice_in)
