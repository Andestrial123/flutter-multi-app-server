import datetime
import uuid

from sqlmodel import SQLModel


class MarkWorkingHoursSchema(SQLModel):
    open_at: datetime.time
    close_at: datetime.time
    is_open: bool = False


class MarkGetSchema(SQLModel):
    id: uuid.UUID
    address: str
    latitude: float
    longitude: float
    bakery_hours: MarkWorkingHoursSchema
    delivery_hours: MarkWorkingHoursSchema
