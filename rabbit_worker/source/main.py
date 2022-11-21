import asyncio

from aiosmtplib import SMTPRecipientsRefused
from pika import BasicProperties
from pika.channel import Channel
from pika.spec import Basic

from core.config import get_settings
from decorators import sync
from rabbitmq import Consumer
from smtp import init_smtp
from email.parser import BytesParser

settings = get_settings()
parser = BytesParser()


@sync
async def send_notification(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    message = parser.parsebytes(body)
    try:
        await email_client.sendmail(message.get('From'), message.get('To'), message.as_string())
        return True
    except SMTPRecipientsRefused:
        return False


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    email_client = loop.run_until_complete(init_smtp(settings.mail_config))
    consumer = Consumer(settings)
    consumer.set_on_message_callback(send_notification)

    try:
        consumer.start()
    finally:
        consumer.stop()
