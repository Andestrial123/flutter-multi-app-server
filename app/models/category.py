import uuid
from typing import Optional

from sqlmodel import SQLModel, Field


class CategoryCreateBase(SQLModel):
    name: str


class CategoryUpdateBase(CategoryCreateBase):
    pass


class CategoryReadBase(CategoryUpdateBase):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True)
    default: bool = False


class Category(CategoryReadBase, table=True):
    pass
