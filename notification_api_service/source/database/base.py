from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.db_config.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()


async def init_tables():
    """
    Создание таблиц в PostgreSQL
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def async_session_generator():
    return sessionmaker(
        engine, class_=AsyncSession
    )


@asynccontextmanager
async def get_session():
    """
    Получить сессию БД. Будет использоваться в Depends.
    """
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception as error:
        await session.rollback()
        raise error
    finally:
        await session.close()
