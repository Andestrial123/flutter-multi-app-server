import uuid
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.translation import TranslationBase


class CategoryCreateBase(SQLModel):
    pass


class CategoryUpdateBase(CategoryCreateBase):
    pass


class CategoryReadBase(CategoryUpdateBase):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True)
    default: bool = False


class Category(CategoryReadBase, table=True):
    products: List["Product"] = Relationship(back_populates="category")
    translations: List["CategoryTranslation"] = Relationship(back_populates="category")
    translation: Optional["CategoryTranslation"] = Relationship()

    @property
    def name(self) -> str:
        if not self.translation:
            return ""

        return self.translation.name


class CategoryTranslation(TranslationBase, table=True):
    __tablename__ = "category_translation"
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True, foreign_key="category.id")

    name: str

    category: Category = Relationship(back_populates="translations")
