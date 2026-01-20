from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class StatementInvoiceItem(BaseModel):
    invoice_id: int
    student_id: int
    student_name: str
    amount: Decimal
    total_paid: Decimal
    balance: Decimal
    status: str
    due_date: date


class SchoolStatement(BaseModel):
    school_id: int
    school_name: str
    students_count: int
    total_invoiced: Decimal
    total_paid: Decimal
    total_pending: Decimal
    invoices: list[StatementInvoiceItem]


class StudentStatement(BaseModel):
    student_id: int
    student_name: str
    school_id: int
    school_name: str
    total_invoiced: Decimal
    total_paid: Decimal
    total_pending: Decimal
    invoices: list[StatementInvoiceItem]
