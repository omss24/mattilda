"""Student management service."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import EntityNotFoundError, ValidationError
from app.models.school import School
from app.models.student import Student
from app.models.student import StudentStatus
from app.schemas.student import StudentCreate, StudentUpdate
from app.utils.pagination import paginate


def ensure_valid_student_status(status: str | StudentStatus) -> StudentStatus:
    if isinstance(status, StudentStatus):
        return status
    try:
        return StudentStatus(status)
    except ValueError as exc:
        raise ValidationError("Invalid student status") from exc


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def list_students(
    db: Session, limit: int, offset: int, school_id: int | None = None
) -> dict:
    base_query = select(Student)

    if school_id is not None:
        base_query = base_query.where(Student.school_id == school_id)

    return paginate(base_query, db, limit, offset)


def create_student(db: Session, student_in: StudentCreate) -> Student:
    """Create a new student.
    
    Business Rules:
    - School must exist
    - Status must be a valid StudentStatus enum value
    """
    school = db.get(School, student_in.school_id)
    if not school:
        raise EntityNotFoundError("School", student_in.school_id)

    status = ensure_valid_student_status(student_in.status)
    student_data = student_in.model_dump()
    student_data["status"] = status
    student = Student(**student_data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student_id: int, student_in: StudentUpdate) -> Student | None:
    student = db.get(Student, student_id)
    if not student:
        return None
    updates = student_in.model_dump(exclude_unset=True)
    if "status" in updates:
        updates["status"] = ensure_valid_student_status(updates["status"])
    for field, value in updates.items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student_id: int) -> bool:
    student = db.get(Student, student_id)
    if not student:
        return False
    db.delete(student)
    db.commit()
    return True
