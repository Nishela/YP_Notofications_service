import asyncio

from pika import BasicProperties
from pika.channel import Channel
from pika.spec import Basic

from core.config import get_settings
from rabbitmq import Consumer
from smtp import init_smtp
settings = get_settings()


def queue_distribution(channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    print(email_client, method.routing_key, body)
    return True


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    email_client = loop.run_until_complete(init_smtp(settings.mail_config))
    consumer = Consumer(settings)
    consumer.set_on_message_callback(queue_distribution)

    try:
        consumer.start()
    except KeyboardInterrupt:
        consumer.stop()
