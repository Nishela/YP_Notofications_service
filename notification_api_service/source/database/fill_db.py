from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from database.base import get_session, Base, engine
from database.tables import Templates, Notifications
from core.config import get_settings
from default_templates import HTML_MAPPER

settings = get_settings()

__all__ = (
    'init_tables',
    'init_notifications',
)


async def init_tables():
    """
    Создание таблиц в PostgreSQL
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def init_notifications():
    async with get_session() as session:
        for notification_type in settings.notification_types:
            item = await session.execute(
                select(Notifications)
                .where(Notifications.name == notification_type.value)
            )

            if not item.first():
                notification_data = (uuid4(), notification_type.value)

                await session.execute(
                    insert(Notifications)
                    .values(notification_data)
                    .on_conflict_do_nothing()
                )

                await session.execute(
                    insert(Templates).
                    values((uuid4(), HTML_MAPPER.get(notification_type), notification_data[0]))
                    .on_conflict_do_nothing()
                )
