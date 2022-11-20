from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

from core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.db_config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()


def async_session_generator():
    return sessionmaker(
        engine, class_=AsyncSession
    )


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception as error:
        await session.rollback()
        raise error
    finally:
        await session.close()
