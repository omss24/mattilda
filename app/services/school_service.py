from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate
from app.utils.pagination import paginate


def get_school(db: Session, school_id: int) -> School | None:
    return db.get(School, school_id)


def list_schools(db: Session, limit: int, offset: int) -> dict:
    query = select(School)
    return paginate(query, db, limit, offset)


def create_school(db: Session, school_in: SchoolCreate) -> School:
    school = School(**school_in.model_dump())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


def update_school(db: Session, school_id: int, school_in: SchoolUpdate) -> School | None:
    school = db.get(School, school_id)
    if not school:
        return None
    for field, value in school_in.model_dump(exclude_unset=True).items():
        setattr(school, field, value)
    db.commit()
    db.refresh(school)
    return school


def delete_school(db: Session, school_id: int) -> bool:
    school = db.get(School, school_id)
    if not school:
        return False
    db.delete(school)
    db.commit()
    return True
