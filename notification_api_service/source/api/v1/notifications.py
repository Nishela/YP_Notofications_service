from http import HTTPStatus

from fastapi import APIRouter, Depends

from core.config import get_settings
from models import EmailModel
from smtp_server.server import get_server

router = APIRouter()
settings = get_settings()


@router.post('/send_notification', response_model=HTTPStatus, summary='Create task for send message')
async def send_with_template(email: EmailModel, server=Depends(get_server)):
    message = await email.Config.builder.async_build(email)  # переделать
    # TODO: тут надо создать таск и положить в очередь rabbit
    await server.sendmail(message.get('From'), message.get('To'), message.as_string())

    return HTTPStatus.OK
