import uuid
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

from app.models.category import Category
from app.models.enums import Unit
from app.models.translation import TranslationBase


class ProductIngredientLink(SQLModel, table=True):
    __tablename__ = "product_ingredient_link"

    ingredient_id: uuid.UUID = Field(foreign_key="ingredient.id", primary_key=True)
    product_id: uuid.UUID = Field(foreign_key="product.id", primary_key=True)


class ProductCreateBase(SQLModel):
    category_id: uuid.UUID = Field(foreign_key="category.id")
    image_url: str
    unit: Unit
    price: float
    calories: float
    quantity: int


class ProductUpdateBase(ProductCreateBase):
    pass


class ProductReadBase(ProductCreateBase):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True)


class Product(ProductReadBase, table=True):
    category: Category = Relationship(back_populates="products")
    ingredients: List["Ingredient"] = Relationship(back_populates="products", link_model=ProductIngredientLink)
    translations: List["ProductTranslation"] = Relationship(back_populates="product")
    translation: Optional["ProductTranslation"] = Relationship()

    @property
    def name(self) -> str:
        if not self.translation:
            return ""

        return self.translation.name

    @property
    def description(self) -> str:
        if not self.translation:
            return ""

        return self.translation.description


class ProductTranslation(TranslationBase, table=True):
    __tablename__ = "product_translation"

    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True, foreign_key="product.id")
    name: str
    description: str

    product: Optional[Product] = Relationship(back_populates="translations")
