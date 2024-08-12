import uuid
from typing import List

from fastapi import Depends, HTTPException

from app.controllers.discount import DiscountController
from app.endpoints.schemas.discount import DiscountGetSchema
from app.endpoints.v1 import router_v1
from app.utils.file import get_name

TAG = get_name(__file__)


@router_v1.get("/discounts", tags=[TAG])
async def get_discounts(
        controller: DiscountController = Depends(DiscountController)) -> List[DiscountGetSchema]:
    discounts = await controller.get_all()
    response = []

    for discount in discounts:
        response.append(DiscountGetSchema.model_validate(discount))

    return response


@router_v1.get("/discount/{discount_id}", tags=[TAG])
async def get_discount(
        discount_id: uuid.UUID,
        controller: DiscountController = Depends(DiscountController)
) -> DiscountGetSchema:
    discount = await controller.get_by_id(discount_id)

    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")

    return DiscountGetSchema.model_validate(discount)
