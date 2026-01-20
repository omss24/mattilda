from app.models.invoice import Invoice
from app.models.payment import Payment
from app.models.school import School
from app.models.student import Student


def test_school_fixture(school: School) -> None:
    assert school.id is not None


def test_student_fixture(school: School, student: Student) -> None:
    assert student.school_id == school.id


def test_invoice_fixture(school: School, student: Student, invoice: Invoice) -> None:
    assert invoice.student_id == student.id
    assert invoice.school_id == school.id


def test_payments_fixture(invoice: Invoice, payments: list[Payment]) -> None:
    assert len(payments) == 2
    assert all(payment.invoice_id == invoice.id for payment in payments)
