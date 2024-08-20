from sqlmodel import SQLModel, Field

from app.models.enums import LanguageCode


class TranslationBase(SQLModel):
    language_code: LanguageCode = Field(primary_key=True)
