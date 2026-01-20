from decimal import Decimal

from pydantic import BaseModel


class InvoiceBalance(BaseModel):
    amount: Decimal
    total_paid: Decimal
    balance: Decimal
    status: str
