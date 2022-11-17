import aiosmtplib
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notifications
from core.config import get_settings
from smtp_server import server

settings = get_settings()

app = FastAPI(
    title=settings.app.project_name,
    docs_url='/notifications/openapi',
    openapi_url='/notifications/openapi.json',
    default_response_class=ORJSONResponse,

)


@app.on_event('startup')
async def startup():
    server.email_client = aiosmtplib.SMTP(
        hostname=settings.mail_config.MAIL_SERVER,
        port=settings.mail_config.MAIL_PORT,
        use_tls=True,
        validate_certs=False
    )
    await server.email_client.connect()
    await server.email_client.login(settings.mail_config.MAIL_USERNAME, settings.mail_config.MAIL_PASSWORD)


@app.on_event('shutdown')
async def shutdown():
    await server.email_client.close()


app.include_router(notifications.router, prefix='/api/v1/notifications', tags=['notifications'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8001,
        # log_config=settings.app.logging,
        # log_level=logging.DEBUG,
    )
