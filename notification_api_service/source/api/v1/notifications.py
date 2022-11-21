from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.config import get_settings
from models import EmailModel
from models.model_utils.email_builder import EmailBuilder
from rabbit_producer.rabbit_utils import get_mq_producer

router = APIRouter()
settings = get_settings()


@router.post('/send_notification', response_model=HTTPStatus, summary='Create task for send message')
async def send_with_template(email: EmailModel, producer=Depends(get_mq_producer)):
    if not (queue_name := settings.queue_types.get(email.notification_type)):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': f'Incorrect notification type - {email.notification_type}'}
        )

    template = ''  # TODO: тут должен быть запрос шаблона из БД
    message = await EmailBuilder.async_build(email, template)

    # кладем задачу в очередь
    await producer.async_publish(routing_key=queue_name, body=message.as_string())  # возможно потребуется правка

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'SUCCESS'}
    )

# TODO: предусмотреть апи для неотправленных сообщений, чтобы добавить их в БД
