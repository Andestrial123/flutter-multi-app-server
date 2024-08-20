import uuid
from typing import List, Optional

from sqlalchemy import or_, func, and_
from sqlalchemy.orm import joinedload, contains_eager
from sqlmodel import select

from app.controllers.base import BaseController
from app.models.category import CategoryTranslation, Category
from app.models.enums import LanguageCode
from app.models.product import Product, ProductTranslation


class ProductController(BaseController):

    async def get_all(self, language_code: LanguageCode,
                      category_id: uuid.UUID = None,
                      search: str = None,
                      ) -> List[Product]:
        filter_options = []

        if category_id:
            filter_options.append(Product.category_id == category_id)

        if search:
            filter_options.append(or_(func.lower(ProductTranslation.name).contains(search.lower()),
                                      func.lower(ProductTranslation.description).contains(search.lower())))

        query = select(Product) \
            .join(Category) \
            .join(CategoryTranslation, onclause=and_(CategoryTranslation.id == Category.id,
                                                     CategoryTranslation.language_code == language_code)) \
            .join(ProductTranslation, onclause=and_(ProductTranslation.id == Product.id,
                                                    ProductTranslation.language_code == language_code)) \
            .where(*filter_options) \
            .options(contains_eager(Product.category).contains_eager(Category.translation),
                     joinedload(Product.ingredients),
                     contains_eager(Product.translation), )

        result = await self._session.execute(query)
        products = result.unique().scalars().all()

        return products

    async def get_by_id(self, product_id: uuid.UUID,
                        language_code: LanguageCode) -> Optional[Product]:
        query = select(Product) \
            .join(Category) \
            .join(CategoryTranslation, onclause=and_(CategoryTranslation.id == Category.id,
                                                     CategoryTranslation.language_code == language_code)) \
            .join(ProductTranslation, onclause=and_(ProductTranslation.id == Product.id,
                                                    ProductTranslation.language_code == language_code)) \
            .where(Product.id == product_id) \
            .options(contains_eager(Product.category).contains_eager(Category.translation),
                     joinedload(Product.ingredients),
                     contains_eager(Product.translation), )

        result = await self._session.execute(query)
        product = result.scalars().first()

        return product
