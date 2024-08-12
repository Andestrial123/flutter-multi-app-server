import uuid
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from app.models.product import ProductIngredientLink, Product


class IngredientCreateBase(SQLModel):
    name: str
    image_url: str


class IngredientUpdateBase(IngredientCreateBase):
    pass


class IngredientReadBase(IngredientUpdateBase):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True)


class Ingredient(IngredientReadBase, table=True):
    products: List[Product] = Relationship(back_populates="ingredients", link_model=ProductIngredientLink)
