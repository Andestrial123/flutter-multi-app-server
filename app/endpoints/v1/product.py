from typing import List

from fastapi import Depends

from app.controllers.product import ProductController
from app.endpoints.schemas.product import ProductGetSchema
from app.endpoints.v1 import router_v1
from app.utils.file import get_name

TAG = get_name(__file__)


@router_v1.get("/products", tags=[TAG])
async def get_products(
        controller: ProductController = Depends(ProductController),
) -> List[ProductGetSchema]:
    products = await controller.get_all()

    response = []

    for product in products:
        response.append(ProductGetSchema.model_validate(product))

    return response
