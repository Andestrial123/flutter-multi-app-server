import uuid
from typing import List

from fastapi import Depends, HTTPException

from app.controllers.category import CategoryController
from app.endpoints.schemas.category import CategoryGetSchema
from app.endpoints.v1 import router_v1
from app.models.enums import LanguageCode
from app.utils.file import get_name
from app.utils.header import accept_language_header

TAG = get_name(__file__)


@router_v1.get("/categories", tags=[TAG])
async def get_categories(
        language_code: LanguageCode = Depends(accept_language_header),
        controller: CategoryController = Depends(CategoryController)) -> List[CategoryGetSchema]:
    categories = await controller.get_all(language_code=language_code)
    response = []

    for category in categories:
        response.append(CategoryGetSchema.model_validate(category))

    return response


@router_v1.get("/category/{category_id}", tags=[TAG])
async def get_category(
        category_id: uuid.UUID,
        language_code: LanguageCode = Depends(accept_language_header),
        controller: CategoryController = Depends(CategoryController)) -> CategoryGetSchema:
    category = await controller.get_by_id(category_id=category_id,
                                          language_code=language_code)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return CategoryGetSchema.model_validate(category)
