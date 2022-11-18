from http import HTTPStatus

from fastapi import APIRouter

from core.config import get_settings
from models import EmailModel
from models.model_utils.email_builder import EmailBuilder

router = APIRouter()
settings = get_settings()


@router.post('/send_notification', response_model=HTTPStatus, summary='Create task for send message')
async def send_with_template(email: EmailModel):
    message = await EmailBuilder.async_build_by_template(email)
    # TODO: тут надо создать таск и положить в очередь rabbit
    return HTTPStatus.OK
