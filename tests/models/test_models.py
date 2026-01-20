from decimal import Decimal

from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.models.payment import Payment


def test_models_and_invoice_balance(
    db_session: Session, invoice: Invoice, payments: list[Payment]
) -> None:
    session = db_session

    session.refresh(invoice)
    balance_info = invoice.calculate_balance()

    assert balance_info.total_paid == Decimal("500.00")
    assert balance_info.balance == Decimal("500.00")
    assert balance_info.status == "partially_paid"
