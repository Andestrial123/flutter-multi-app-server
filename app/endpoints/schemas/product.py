from typing import List, Type, Any, Union, Dict

from sqlmodel.main import _TSQLModel

from app.endpoints.schemas.category import CategoryGetSchema
from app.endpoints.schemas.ingredient import IngredientGetSchema
from app.models.product import ProductReadBase
from app.utils.translation.wrapper import translated


class ProductGetSchema(ProductReadBase):
    name: str
    description: str
    category: CategoryGetSchema
    ingredients: List[IngredientGetSchema]