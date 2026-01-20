from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.invoice import InvoiceStatus


class InvoiceBase(BaseModel):
    school_id: int
    student_id: int
    issue_date: date
    due_date: date
    amount: Decimal = Field(ge=0)
    currency: str = "MXN"
    status: InvoiceStatus = InvoiceStatus.pending
    description: str | None = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    issue_date: date | None = None
    due_date: date | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    currency: str | None = None
    status: InvoiceStatus | None = None
    description: str | None = None


class InvoiceRead(InvoiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
