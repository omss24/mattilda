from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.cache import build_cache_key, cache_get, cache_set
from app.core.db import get_db
from app.core.security import verify_api_key
from app.schemas.pagination import PaginatedResponse
from app.schemas.school import SchoolCreate, SchoolRead, SchoolUpdate
from app.schemas.statement import SchoolStatement
from app.services.school_service import (
    create_school,
    delete_school,
    get_school,
    list_schools,
    update_school,
)
from app.services.statement_service import get_school_statement

router = APIRouter(
    prefix="/schools", tags=["schools"], dependencies=[Depends(verify_api_key)]
)


@router.post("", response_model=SchoolRead, status_code=status.HTTP_201_CREATED)
def create_school_endpoint(
    school_in: SchoolCreate, db: Session = Depends(get_db)
) -> SchoolRead:
    return create_school(db, school_in)


@router.get("", response_model=PaginatedResponse[SchoolRead])
def list_schools_endpoint(
    limit: int = 10, offset: int = 0, db: Session = Depends(get_db)
) -> PaginatedResponse[SchoolRead]:
    result = list_schools(db, limit=limit, offset=offset)
    return PaginatedResponse(**result)


@router.get("/{school_id}", response_model=SchoolRead)
def get_school_endpoint(school_id: int, db: Session = Depends(get_db)) -> SchoolRead:
    school = get_school(db, school_id)
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    return school


@router.put("/{school_id}", response_model=SchoolRead)
def update_school_endpoint(
    school_id: int, school_in: SchoolUpdate, db: Session = Depends(get_db)
) -> SchoolRead:
    school = update_school(db, school_id, school_in)
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    return school


@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_endpoint(school_id: int, db: Session = Depends(get_db)) -> None:
    deleted = delete_school(db, school_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")


@router.get("/{school_id}/statement", response_model=SchoolStatement)
def get_school_statement_endpoint(
    school_id: int, request: Request, db: Session = Depends(get_db)
) -> SchoolStatement:
    cache_key = build_cache_key(request)
    cached = cache_get(cache_key)
    if cached:
        return cached
    statement = get_school_statement(db, school_id)
    if not statement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="School not found")
    cache_set(cache_key, statement.model_dump(mode="json"))
    return statement
