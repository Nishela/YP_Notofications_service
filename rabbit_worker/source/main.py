import asyncio

from pika import BasicProperties
from pika.channel import Channel

from core.config import get_settings
from rabbitmq import Consumer
from smtp import init_smtp
settings = get_settings()


def queue_distribution(channel: Channel, method, properties: BasicProperties, body: bytes):
    # channel.confirm_delivery()
    print(email_client, method.routing_key, body)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    email_client = loop.run_until_complete(init_smtp(settings.mail_config))
    consumer = Consumer(settings.rabbitmq)
    consumer.set_on_message_callback(queue_distribution)
    try:
        consumer.start()
    except KeyboardInterrupt:
        consumer.stop()
