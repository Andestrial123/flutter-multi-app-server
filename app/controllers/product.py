from typing import List

from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.controllers.base import BaseController
from app.models.product import Product


class ProductController(BaseController):

    async def get_all(self) -> List[Product]:
        query = select(Product) \
            .options(joinedload(Product.category),
                     joinedload(Product.ingredients))

        result = await self._session.execute(query)
        products = result.unique().scalars().all()

        return products
