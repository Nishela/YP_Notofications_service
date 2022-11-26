from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.db_config.database_uri)

Base = declarative_base()


def async_session_generator():
    return sessionmaker(
        engine, class_=AsyncSession
    )


@asynccontextmanager
async def get_session():
    """
    Получить сессию БД.
    """
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
            await session.commit()
    except Exception as error:
        await session.rollback()
        raise error
    finally:
        await session.close()
