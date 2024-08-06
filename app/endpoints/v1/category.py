import uuid
from typing import List

from fastapi import Depends, HTTPException

from app.controllers.category import CategoryController
from app.endpoints.schemas.category import CategoryGetSchema
from app.endpoints.v1 import router_v1
from app.utils.file import get_name

TAG = get_name(__file__)


@router_v1.get("/categories", tags=[TAG])
async def get_categories(controller: CategoryController = Depends(CategoryController)) -> List[CategoryGetSchema]:
    categories = await controller.get_all()
    response = []

    for category in categories:
        response.append(CategoryGetSchema.model_validate(category))

    return response


@router_v1.get("/category/{category_id}", tags=[TAG])
async def get_category(
        category_id: uuid.UUID,
        controller: CategoryController = Depends(CategoryController)) -> CategoryGetSchema:
    category = await controller.get_by_id(category_id=category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return CategoryGetSchema.model_validate(category)
