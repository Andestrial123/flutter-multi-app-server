import uuid
from typing import List, Optional

from fastapi import Depends, HTTPException

from app.controllers.product import ProductController
from app.endpoints.schemas.product import ProductGetSchema
from app.endpoints.v1 import router_v1
from app.utils.file import get_name

TAG = get_name(__file__)


@router_v1.get("/products", tags=[TAG])
async def get_products(
        category_id: Optional[uuid.UUID] = None,
        search: Optional[str] = None,
        controller: ProductController = Depends(ProductController),
) -> List[ProductGetSchema]:
    products = await controller.get_all(category_id=category_id,
                                        search=search)

    response = []

    for product in products:
        response.append(ProductGetSchema.model_validate(product))

    return response


@router_v1.get("/products/{product_id}", tags=[TAG])
async def get_product(product_id: uuid.UUID,
                      controller: ProductController = Depends(ProductController)) -> ProductGetSchema:
    product = await controller.get_by_id(product_id=product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductGetSchema.model_validate(product)
