from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import row

from database.base import get_session
from database.tables import Notifications, Templates
from models.template_model import TemplateModel

__all__ = (
    'DbManager',
)


class DbManager:

    @classmethod
    async def async_get_template(cls, notification_name: str = '', template_id: str = '') -> str or row:
        """
        Получение шаблона для полученного типа уведомления

        :param notification_name: str
        :param template_id: str
        :return: str
        """
        async with get_session() as session:
            if notification_name and not template_id:
                result = await session.execute(
                    select(Templates).join(Notifications, Templates.notification_id == Notifications.id)
                    .where(Notifications.name == notification_name)
                )
            else:
                result = await session.execute(
                    select(Templates).where(Templates.id == template_id)
                )
            return result.first()[0]

    @classmethod
    async def async_add_template(cls, template: TemplateModel) -> bool:
        success = False
        async with get_session() as session:
            await session.execute(
                insert(Templates)
                .values(**template.dict())
                .on_conflict_do_nothing()
            )
            return True if success else False

    @classmethod
    async def async_delete_template(cls, template: TemplateModel) -> bool:
        success = False
        async with get_session() as session:
            await session.execute(
                delete(Templates)
                .where(Templates.id == str(template.id))
            )
            return True if success else False

    @classmethod
    async def async_update_template(cls, template: TemplateModel) -> bool:
        success = False
        args = {key: val for key, val in template.dict().items() if (key != 'id' and key)}
        async with get_session() as session:
            await session.execute(
                update(Templates)
                .where(Templates.id == str(template.id))
                .values(**args)
            )
            return True if success else False
