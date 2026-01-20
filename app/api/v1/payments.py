from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import verify_api_key
from app.schemas.pagination import PaginatedResponse
from app.schemas.payment import PaymentCreate, PaymentRead
from app.services.payment_service import create_payment, get_payment, list_payments

router = APIRouter(
    prefix="/payments", tags=["payments"], dependencies=[Depends(verify_api_key)]
)


@router.post("", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment_endpoint(
    payment_in: PaymentCreate, db: Session = Depends(get_db)
) -> PaymentRead:
    return create_payment(db, payment_in)


@router.get("", response_model=PaginatedResponse[PaymentRead])
def list_payments_endpoint(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    invoice_id: int | None = None,
    student_id: int | None = None,
    school_id: int | None = None,
    db: Session = Depends(get_db),
) -> PaginatedResponse[PaymentRead]:
    result = list_payments(
        db,
        limit=limit,
        offset=offset,
        invoice_id=invoice_id,
        student_id=student_id,
        school_id=school_id,
    )
    return PaginatedResponse(**result)


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment_endpoint(payment_id: int, db: Session = Depends(get_db)) -> PaymentRead:
    payment = get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment
