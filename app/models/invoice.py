from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Enum as SqlEnum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.payment import Payment
    from app.models.school import School
    from app.models.student import Student
    from app.schemas.invoice_balance import InvoiceBalance


class InvoiceStatus(str, Enum):
    """Invoice lifecycle states.
    
    Transitions: pending → partially_paid → paid (terminal)
                 Any state → cancelled (terminal)
    """
    pending = "pending"
    partially_paid = "partially_paid"
    paid = "paid"
    cancelled = "cancelled"


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="MXN")
    status: Mapped[InvoiceStatus] = mapped_column(
        SqlEnum(InvoiceStatus, name="invoice_status"),
        default=InvoiceStatus.pending,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    school: Mapped[School] = relationship(back_populates="invoices")
    student: Mapped[Student] = relationship(back_populates="invoices")
    payments: Mapped[list[Payment]] = relationship(
        back_populates="invoice", cascade="all, delete-orphan"
    )

    def calculate_balance(self) -> "InvoiceBalance":
        """
        Based on the payments made, calculate the total paid amount, remaining balance and
        current status of the invoice.
        """
        from app.schemas.invoice_balance import InvoiceBalance

        payments = self.payments or []
        total_paid = sum((payment.amount for payment in payments), Decimal("0"))
        balance = self.amount - total_paid

        if self.status == InvoiceStatus.cancelled:
            computed_status = InvoiceStatus.cancelled
        elif balance <= Decimal("0"):
            computed_status = InvoiceStatus.paid
        elif balance < self.amount:
            computed_status = InvoiceStatus.partially_paid
        else:
            computed_status = InvoiceStatus.pending

        return InvoiceBalance(
            amount=self.amount,
            total_paid=total_paid,
            balance=balance,
            status=computed_status.value,
        )
