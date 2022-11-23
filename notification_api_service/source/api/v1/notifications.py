from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.config import get_settings, NotificationTypes
from models import EmailModel
from models.model_utils.email_builder import EmailBuilder
from rabbit_producer.rabbit_utils import get_mq_producer

router = APIRouter()
settings = get_settings()


@router.post('/send_email', response_model=Any, summary='Create task for send message')
async def send_with_template(email: EmailModel, notification_type: NotificationTypes,
                             producer=Depends(get_mq_producer), use_template: bool = True) -> JSONResponse:
    """
        ## Create task for send email message:
        - _email_ - Модель email сообщения
        - _notification_type_ - тип уведомления для которого создается email сообщение
        - _use_template_ - Флаг использования html шаблона при сборке email сообщения

    """
    template = ''
    if use_template:
        if not (template := await email.Config.db_manager.async_get_template(notification_type.value)):
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={'message': f'Template not found - {notification_type.value}'}
            )

    message = await EmailBuilder.async_build(email, template)
    await producer.async_publish(routing_key=notification_type.value, body=message.as_string())

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'SUCCESS'}
    )
