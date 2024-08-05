from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.db import db


class BaseController:

    def __init__(self, session: AsyncSession = Depends(db)):
        self._session = session
