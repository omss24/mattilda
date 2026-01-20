from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.invoice import Invoice, InvoiceStatus
from app.models.school import School
from app.models.student import Student
from app.schemas.statement import SchoolStatement, StatementInvoiceItem, StudentStatement


def get_school_statement(db: Session, school_id: int) -> SchoolStatement | None:
    school = db.get(School, school_id)
    if not school:
        return None

    invoices = db.scalars(
        select(Invoice)
        .where(Invoice.school_id == school_id)
        .options(
            selectinload(Invoice.payments),
            selectinload(Invoice.student),
        )
    ).all()

    students_count = db.scalar(
        select(func.count()).select_from(Student).where(Student.school_id == school_id)
    ) or 0

    total_invoiced = Decimal("0")
    total_paid = Decimal("0")
    items: list[StatementInvoiceItem] = []

    for invoice in invoices:
        balance_info = invoice.calculate_balance()
        if balance_info.status != InvoiceStatus.cancelled.value:
            total_invoiced += invoice.amount
            total_paid += balance_info.total_paid

        items.append(
            StatementInvoiceItem(
                invoice_id=invoice.id,
                student_id=invoice.student_id,
                student_name=f"{invoice.student.first_name} {invoice.student.last_name}",
                amount=invoice.amount,
                total_paid=balance_info.total_paid,
                balance=balance_info.balance,
                status=balance_info.status,
                due_date=invoice.due_date,
            )
        )

    total_pending = total_invoiced - total_paid

    return SchoolStatement(
        school_id=school.id,
        school_name=school.name,
        students_count=students_count,
        total_invoiced=total_invoiced,
        total_paid=total_paid,
        total_pending=total_pending,
        invoices=items,
    )


def get_student_statement(db: Session, student_id: int) -> StudentStatement | None:
    student = db.get(Student, student_id)
    if not student:
        return None

    invoices = db.scalars(
        select(Invoice)
        .where(Invoice.student_id == student_id)
        .options(
            selectinload(Invoice.payments),
            selectinload(Invoice.school),
        )
    ).all()

    total_invoiced = Decimal("0")
    total_paid = Decimal("0")
    items: list[StatementInvoiceItem] = []

    for invoice in invoices:
        balance_info = invoice.calculate_balance()
        if balance_info.status != InvoiceStatus.cancelled.value:
            total_invoiced += invoice.amount
            total_paid += balance_info.total_paid

        items.append(
            StatementInvoiceItem(
                invoice_id=invoice.id,
                student_id=invoice.student_id,
                student_name=f"{student.first_name} {student.last_name}",
                amount=invoice.amount,
                total_paid=balance_info.total_paid,
                balance=balance_info.balance,
                status=balance_info.status,
                due_date=invoice.due_date,
            )
        )

    total_pending = total_invoiced - total_paid

    return StudentStatement(
        student_id=student.id,
        student_name=f"{student.first_name} {student.last_name}",
        school_id=student.school_id,
        school_name=student.school.name,
        total_invoiced=total_invoiced,
        total_paid=total_paid,
        total_pending=total_pending,
        invoices=items,
    )
