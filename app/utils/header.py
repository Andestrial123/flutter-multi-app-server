from fastapi import Header

from app.models.enums import LanguageCode


def accept_language_header(accept_language: str = Header(
    default="en",
    alias="accept-language",
    description="Supported languages are: en, uk. "
                "All other values will be ignored and en translation will be used for response",
    convert_underscores=False,
    include_in_schema=True)
) -> LanguageCode:
    if LanguageCode.uk in accept_language:
        return LanguageCode.uk
    return LanguageCode.en
