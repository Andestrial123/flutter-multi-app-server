import uuid
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import contains_eager
from sqlmodel import select

from app.controllers.base import BaseController
from app.models.category import Category, CategoryTranslation
from app.models.enums import LanguageCode


class CategoryController(BaseController):

    async def get_all(self, language_code: LanguageCode) -> List[Category]:
        query = select(Category) \
            .join(CategoryTranslation, onclause=and_(CategoryTranslation.id == Category.id,
                                                     CategoryTranslation.language_code == language_code)) \
            .options(contains_eager(Category.translation))

        result = await self._session.execute(query)
        categories: List[Category] = result.scalars().all()

        return categories

    async def get_by_id(self, category_id: uuid.UUID,
                        language_code: LanguageCode) -> Optional[Category]:
        query = select(Category) \
            .join(CategoryTranslation, onclause=and_(CategoryTranslation.id == Category.id,
                                                     CategoryTranslation.language_code == language_code)) \
            .where(Category.id == category_id) \
            .options(contains_eager(Category.translation))

        result = await self._session.execute(query)
        category = result.scalars().first()

        return category
