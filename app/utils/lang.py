from fastapi import Header

accept_language_header = Header(
    default="en",
    alias="accept-language",
    description="Supported languages are: en, uk. "
                "All other values will be ignored and en translation will be used for response",
    convert_underscores=False,
    include_in_schema=True)
