from typing import List

from app.endpoints.schemas.category import CategoryGetSchema
from app.endpoints.schemas.ingredient import IngredientGetSchema
from app.models.product import ProductReadBase


class ProductGetSchema(ProductReadBase):
    category: CategoryGetSchema
    ingredients: List[IngredientGetSchema]
