import pytest
from sqlalchemy.exc import IntegrityError

from app.models.school import School
from app.models.student import StudentStatus
from app.schemas.school import SchoolCreate
from app.schemas.student import StudentCreate
from app.services.school_service import create_school
from app.services.student_service import create_student, ensure_valid_student_status


def test_student_requires_existing_school(db_session):
    student_in = StudentCreate(
        school_id=999,
        first_name="Ana",
        last_name="Lopez",
        status=StudentStatus.active,
    )
    with pytest.raises(ValueError, match="School does not exist"):
        create_student(db_session, student_in)


def test_student_status_must_be_valid():
    with pytest.raises(ValueError, match="Invalid student status"):
        ensure_valid_student_status("invalid")


def test_school_name_required(db_session):
    school = School(name=None)
    db_session.add(school)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_student_with_valid_school(db_session):
    school = create_school(db_session, SchoolCreate(name="Valid School"))
    student_in = StudentCreate(
        school_id=school.id,
        first_name="Ana",
        last_name="Lopez",
        status=StudentStatus.active,
    )
    student = create_student(db_session, student_in)
    assert student.school_id == school.id
