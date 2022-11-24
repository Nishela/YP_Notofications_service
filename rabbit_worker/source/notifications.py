import logging
from email.parser import BytesParser

from aiosmtplib import SMTPRecipientsRefused
from pika import BasicProperties
from pika.channel import Channel
from pika.spec import Basic

from core.config import get_settings
from decorators import sync
from smtp import SMTPClient


class Notifications:
    settings = get_settings()
    parser = BytesParser()
    smtp_client = SMTPClient(settings.mail_config)

    @staticmethod
    @sync
    async def email_notification(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        message = Notifications.parser.parsebytes(body)
        try:
            async with Notifications.smtp_client as client:
                logging.debug('Received message from queue to %s', message.get('To'))
                await client.sendmail(message.get('From'), message.get('To'), message.as_string())
            logging.debug('Message sent')
            return True
        except SMTPRecipientsRefused:
            logging.warning('Message to %s doesn\'t sent', message.get('To'))
            return False

    @staticmethod
    @sync
    async def sms_notification(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        """Future"""
        logging.warning('Future notification handler. Message received:\n%s', body.decode(encoding='utf-8'))
        return True

    @staticmethod
    @sync
    async def push_notification(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        """Future"""
        logging.warning('Future notification handler. Message received:\n%s', body.decode(encoding='utf-8'))
        return True
