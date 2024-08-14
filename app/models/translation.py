import uuid
from typing import Optional

from sqlmodel import SQLModel, Field

from app.models.enums import LanguageCode


class TranslationBase(SQLModel):
    id: Optional[uuid.UUID] = Field(default=uuid.uuid4, primary_key=True, foreign_key="category.id")
    language_code: LanguageCode = Field(primary_key=True)
