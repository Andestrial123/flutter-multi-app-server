import uuid
from typing import List, Optional

from sqlmodel import select

from app.controllers.base import BaseController
from app.models.discount import Discount


class DiscountController(BaseController):

    async def get_all(self) -> List[Discount]:
        query = select(Discount)

        result = await self._session.execute(query)
        categories: List[Discount] = result.scalars().all()

        return categories

    async def get_by_id(self, discount_id: uuid.UUID) -> Optional[Discount]:
        query = select(Discount) \
            .where(Discount.id == discount_id)

        result = await self._session.execute(query)
        category = result.scalars().first()

        return category
