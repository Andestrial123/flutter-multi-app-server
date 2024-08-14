from app.models.category import CategoryReadBase


class CategoryGetSchema(CategoryReadBase):
    name: str
