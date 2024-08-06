import uuid
from typing import List, Optional

from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.controllers.base import BaseController
from app.models.product import Product


class ProductController(BaseController):

    async def get_all(self, category_id: uuid.UUID = None, search: str = None) -> List[Product]:
        filter_options = []

        if category_id:
            filter_options.append(Product.category_id == category_id)

        if search:
            filter_options.append(or_(func.lower(Product.name).contains(search.lower()),
                                      func.lower(Product.description).contains(search.lower())))

        query = select(Product) \
            .where(*filter_options) \
            .options(joinedload(Product.category),
                     joinedload(Product.ingredients))

        result = await self._session.execute(query)
        products = result.unique().scalars().all()

        return products

    async def get_by_id(self, product_id: uuid.UUID) -> Optional[Product]:
        query = select(Product) \
            .where(Product.id == product_id) \
            .options(joinedload(Product.category),
                     joinedload(Product.ingredients))

        result = await self._session.execute(query)
        product = result.scalars().first()

        return product
