from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.student import StudentStatus


class StudentBase(BaseModel):
    school_id: int
    first_name: str
    last_name: str
    external_id: str | None = None
    status: StudentStatus = StudentStatus.active


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    external_id: str | None = None
    status: StudentStatus | None = None


class StudentRead(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
