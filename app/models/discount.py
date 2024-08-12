import uuid
from typing import Optional

from sqlmodel import SQLModel, Field

from app.models.enums import DiscountOpenType


class DiscountCreateBase(SQLModel):
    image_url: str
    open_type: DiscountOpenType
    link: str


class DiscountUpdateBase(DiscountCreateBase):
    pass


class DiscountReadBase(DiscountUpdateBase):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True)


class Discount(DiscountReadBase, table=True):
    pass
