from typing import Type, Any, Union, Dict

from sqlmodel.main import _TSQLModel

from app.models.category import CategoryReadBase
from app.utils.translation.wrapper import translated


class CategoryGetSchema(CategoryReadBase):

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
        return validated
