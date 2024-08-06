from typing import List, Type, Any, Union, Dict

from sqlmodel.main import _TSQLModel

from app.endpoints.schemas.category import CategoryGetSchema
from app.endpoints.schemas.ingredient import IngredientGetSchema
from app.models.product import ProductReadBase
from app.utils.translation.wrapper import translated


class ProductGetSchema(ProductReadBase):
    category: CategoryGetSchema
    ingredients: List[IngredientGetSchema]

    @classmethod
    def model_validate(
            cls: Type[_TSQLModel],
            obj: Any,
            *,
            strict: Union[bool, None] = None,
            from_attributes: Union[bool, None] = None,
            context: Union[Dict[str, Any], None] = None,
            update: Union[Dict[str, Any], None] = None,
    ) -> _TSQLModel:
        validated = super().model_validate(
            obj=obj,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            update=update,
        )
        validated.name = translated(validated.name)
        validated.description = translated(validated.description)
        return validated
