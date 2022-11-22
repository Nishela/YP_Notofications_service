from sqlalchemy.future import select

from database.base import get_session
from database.tables import Notifications, Templates

__all__ = (
    'DbManager',
)


class DbManager:

    @classmethod
    async def async_get_template(cls, notification_name: str) -> str:
        """
        Получение шаблона для полученного типа уведомления

        :param notification_name: str
        :return: str
        """
        async with get_session() as session:
            result = await session.execute(
                select(Templates).join(Notifications, Templates.notification_id == Notifications.id)
                .where(Notifications.name == notification_name)
            )
            return result.first()[0].body

    # TODO: вероятно можно накидать методов записи данных в таблицы, добавление шаблонов и тд
