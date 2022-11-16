from http import HTTPStatus

from fastapi import APIRouter

from core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post('/send_notification', response_model=HTTPStatus, summary='Create task for send message')
async def send_notification(data):
    ...
