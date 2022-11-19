from http import HTTPStatus

from fastapi import APIRouter, Depends

from core.config import get_settings
from models import EmailModel
from models.model_utils.email_builder import EmailBuilder
from rabbit_producer.rabbit_utils import get_mq_producer

router = APIRouter()
settings = get_settings()


@router.post('/send_notification', response_model=HTTPStatus, summary='Create task for send message')
async def send_with_template(email: EmailModel, producer=Depends(get_mq_producer)):
    if not (queue_name := settings.queue_types.get(email.notification_type)):
        return HTTPStatus.NOT_FOUND

    message = await EmailBuilder.async_build_by_template(email)
    await producer.async_publish(routing_key=queue_name, body=message.json())
    return HTTPStatus.OK

# TODO: предусмотреть апи для неотправленных сообщений, чтобы добавить их в БД
