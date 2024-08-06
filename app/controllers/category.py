import uuid
from typing import List, Optional

from sqlmodel import select

from app.controllers.base import BaseController
from app.models.category import Category


class CategoryController(BaseController):

    async def get_all(self) -> List[Category]:
        query = select(Category)

        result = await self._session.execute(query)
        categories: List[Category] = result.scalars().all()

        return categories

    async def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        query = select(Category) \
            .where(Category.id == category_id)

        result = await self._session.execute(query)
        category = result.scalars().first()

        return category
