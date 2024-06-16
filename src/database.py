from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

DATABASE_URL = (f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}"
                f"@{settings.db_host}:{settings.db_port}/{settings.db_name}")


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость с получением сессии БД"""
    async with async_session_maker() as session:
        yield session
