from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.config import PostgresConfig
from app.models.common import BaseModel


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self.async_sessionmaker = None

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    async def __call__(self) -> AsyncIterator[AsyncSession]:
        """For use with FastAPI Depends"""
        if not self.async_sessionmaker:
            raise ValueError("async_sessionmaker not available. Run setup() first.")

        try:
            async with self.async_sessionmaker() as session:
                yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

    def setup(self, config: PostgresConfig):
        self._engine = create_async_engine(
            url=config.url,
            echo=config.echo,
            **config.engine_props
        )
        
        self.async_sessionmaker = sessionmaker(self._engine,
                                               expire_on_commit=False,
                                               autocommit=False,
                                               autoflush=False,
                                               class_=AsyncSession)

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
