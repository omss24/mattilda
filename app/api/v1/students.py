from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.core.cache import build_cache_key, cache_get, cache_set
from app.core.db import get_db
from app.core.security import verify_api_key
from app.schemas.pagination import PaginatedResponse
from app.schemas.statement import StudentStatement
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.services.statement_service import get_student_statement
from app.services.student_service import (
    create_student,
    delete_student,
    get_student,
    list_students,
    update_student,
)

router = APIRouter(
    prefix="/students", tags=["students"], dependencies=[Depends(verify_api_key)]
)


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student_endpoint(
    student_in: StudentCreate, db: Session = Depends(get_db)
) -> StudentRead:
    return create_student(db, student_in)


@router.get("", response_model=PaginatedResponse[StudentRead])
def list_students_endpoint(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    school_id: int | None = None,
    db: Session = Depends(get_db),
) -> PaginatedResponse[StudentRead]:
    result = list_students(db, limit=limit, offset=offset, school_id=school_id)
    return PaginatedResponse(**result)


@router.get("/{student_id}", response_model=StudentRead)
def get_student_endpoint(student_id: int, db: Session = Depends(get_db)) -> StudentRead:
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentRead)
def update_student_endpoint(
    student_id: int, student_in: StudentUpdate, db: Session = Depends(get_db)
) -> StudentRead:
    student = update_student(db, student_id, student_in)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db)) -> None:
    deleted = delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


@router.get("/{student_id}/statement", response_model=StudentStatement)
def get_student_statement_endpoint(
    student_id: int, request: Request, db: Session = Depends(get_db)
) -> StudentStatement:
    cache_key = build_cache_key(request)
    cached = cache_get(cache_key)
    if cached:
        return cached
    statement = get_student_statement(db, student_id)
    if not statement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    cache_set(cache_key, statement.model_dump(mode="json"))
    return statement
