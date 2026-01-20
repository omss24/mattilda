from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import verify_api_key
from app.models.invoice import InvoiceStatus
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.invoice_service import (
    cancel_invoice,
    create_invoice,
    get_invoice,
    list_invoices,
    update_invoice,
)

router = APIRouter(
    prefix="/invoices", tags=["invoices"], dependencies=[Depends(verify_api_key)]
)


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice_endpoint(
    invoice_in: InvoiceCreate, db: Session = Depends(get_db)
) -> InvoiceRead:
    return create_invoice(db, invoice_in)


@router.get("", response_model=PaginatedResponse[InvoiceRead])
def list_invoices_endpoint(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    school_id: int | None = None,
    student_id: int | None = None,
    status: InvoiceStatus | None = None,
    db: Session = Depends(get_db),
) -> PaginatedResponse[InvoiceRead]:
    result = list_invoices(
        db,
        limit=limit,
        offset=offset,
        school_id=school_id,
        student_id=student_id,
        status=status,
    )
    return PaginatedResponse(**result)


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice_endpoint(invoice_id: int, db: Session = Depends(get_db)) -> InvoiceRead:
    invoice = get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceRead)
def update_invoice_endpoint(
    invoice_id: int, invoice_in: InvoiceUpdate, db: Session = Depends(get_db)
) -> InvoiceRead:
    invoice = update_invoice(db, invoice_id, invoice_in)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice


@router.delete("/{invoice_id}", response_model=InvoiceRead)
def cancel_invoice_endpoint(
    invoice_id: int, db: Session = Depends(get_db)
) -> InvoiceRead:
    invoice = cancel_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice
