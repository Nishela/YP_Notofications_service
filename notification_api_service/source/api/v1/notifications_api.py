from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.config import NotificationTypes
from database.managers import get_db_manager, get_auth_manager
from models import EmailModel, PushModel, SmsModel
from models.model_utils import NotificationBuilder
from rabbit_producer.rabbit_utils import get_mq_producer

router = APIRouter()


@router.post('/send_email', response_model=Any, summary='Create task for send email notification')
async def send_email_notification(
        email: EmailModel,
        producer=Depends(get_mq_producer),
        db_manager=Depends(get_db_manager),
        auth_manager=Depends(get_auth_manager),
        use_template: bool = True,
) -> JSONResponse:
    """
        ## Create task for send email notification:
        - _email_ - Модель email уведомления
        - _use_template_ - Флаг использования html шаблона при сборке email уведомления
    """
    template = ''
    if use_template:
        if not (
                template := await db_manager.async_get_template(
                    notification_name=f'{NotificationTypes.EMAIL.value}'
                )
        ):
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={'message': f'Template not found - {NotificationTypes.EMAIL.value}'}
            )
    # отдаем user_id в сервис авторизации для получения информации о пользователе - user_info
    # user_info = await auth_manager.async_get_user_info(email.user_id)
    message = await NotificationBuilder.async_build_email(email, html_template=template)
    await producer.async_publish(routing_key=NotificationTypes.EMAIL.value, body=message.as_string())

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'SUCCESS'}
    )


@router.post('/send_push', response_model=Any, summary='Create task for send push notification')
async def send_push_notification(
        push_notification: PushModel,
        producer=Depends(get_mq_producer),
        db_manager=Depends(get_db_manager),
        auth_manager=Depends(get_auth_manager),
) -> JSONResponse:
    """
        ## Create task for send push notification:
        - _push_notification_ - Модель push уведомления
    """
    if not (template := await db_manager.async_get_template(f'{NotificationTypes.PUSH.value}')):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': f'Template not found - {NotificationTypes.PUSH.value}'}
        )
    # отдаем user_id в сервис авторизации для получения информации о пользователе - user_info
    # user_info = await auth_manager.async_get_user_info(email.user_id)
    message = await NotificationBuilder.async_build_push(push_notification, template)
    await producer.async_publish(routing_key=NotificationTypes.PUSH.value, body=message)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'SUCCESS'}
    )


@router.post('/send_sms', response_model=Any, summary='Create task for send sms notification')
async def send_sms_notification(
        sms_notification: SmsModel,
        producer=Depends(get_mq_producer),
        db_manager=Depends(get_db_manager),
        auth_manager=Depends(get_auth_manager),
) -> JSONResponse:
    """
        ## Create task for send sms notification:
        - _sms_notification_ - Модель sms уведомления
    """
    if not (template := await db_manager.async_get_template(f'{NotificationTypes.SMS.value}')):
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': f'Template not found - {NotificationTypes.SMS.value}'}
        )
    # отдаем user_id в сервис авторизации для получения информации о пользователе - user_info
    # user_info = await auth_manager.async_get_user_info(email.user_id)
    message = await NotificationBuilder.async_build_sms(sms_notification, template)
    await producer.async_publish(routing_key=NotificationTypes.SMS.value, body=message)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': f'SUCCESS'}
    )
