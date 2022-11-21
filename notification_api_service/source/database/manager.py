from sqlalchemy.future import select

from database.base import get_session
from database.tables import Notifications, Templates

__all__ = (
    'DbManager',
)


class DbManager:

    @classmethod
    async def async_get_template(cls, notification_name):
        async with get_session() as session:
            result = await session.execute(
                select(Templates).join(Notifications, Templates.notification_id == Notifications.id)
                .where(Notifications.name == notification_name)
            )
            return result.first()

    # TODO: вероятно можно накидать методов записи данных в таблицы, добавление шаблонов и тд
