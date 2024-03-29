import logging

import aio_pika
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notifications_api, templates_api
from core.config import get_settings
from rabbit_producer import rabbit_utils
from rabbit_producer.producer import RabbitProducer

settings = get_settings()

app = FastAPI(
    title=settings.app.project_name,
    docs_url='/notifications/openapi',
    openapi_url='/notifications/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    rabbit_utils.mq_connection = await aio_pika.connect_robust(**settings.rabbit_config.dict())
    rabbit_utils.mq_producer = await RabbitProducer().async_configure(settings.rabbit_config.exchange_point_name)


@app.on_event('shutdown')
async def shutdown():
    await rabbit_utils.mq_connection.close()


app.include_router(notifications_api.router, prefix='/api/v1/notifications', tags=['Notifications'])
app.include_router(templates_api.router, prefix='/api/v1/templates', tags=['Templates'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8001,
        log_config=settings.app.logging,
        log_level=logging.DEBUG,
    )
