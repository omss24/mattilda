from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    invoice_id: int
    paid_at: datetime
    amount: Decimal = Field(ge=0)
    method: str
    reference: str | None = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    paid_at: datetime | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    method: str | None = None
    reference: str | None = None


class PaymentRead(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
