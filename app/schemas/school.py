from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SchoolBase(BaseModel):
    name: str
    external_id: str | None = None
    address: str | None = None


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(BaseModel):
    name: str | None = None
    external_id: str | None = None
    address: str | None = None


class SchoolRead(SchoolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
