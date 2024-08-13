import datetime
import uuid
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.enums import Day, WorkType


class MarkWorkingHours(SQLModel, table=True):
    __tablename__ = "mark_working_hours"

    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True)
    mark_id: uuid.UUID = Field(foreign_key="mark.id")
    day: Day
    open_at: datetime.time
    close_at: datetime.time
    work_type: WorkType

    mark: 'Mark' = Relationship(back_populates="working_hours")


class MarkCreateBase(SQLModel):
    address: str
    latitude: float
    longitude: float
    image_url: str


class MarkUpdateBase(MarkCreateBase):
    pass


class MarkReadBase(MarkUpdateBase):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)


class Mark(MarkReadBase, table=True):
    working_hours: List[MarkWorkingHours] = Relationship(back_populates="mark")
