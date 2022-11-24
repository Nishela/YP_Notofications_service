import asyncio
import logging

from core.config import get_settings
from notifications import Notifications
from rabbitmq import Consumer

settings = get_settings()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    consumer = Consumer(settings)
    # register queue func handlers
    for queue_name in settings.notification_types:
        consumer.set_on_message_callback(
            getattr(Notifications, f'{queue_name.value}_notification'),
            queue_name.value)
        logging.debug('set callback on queue: %s', queue_name)

    try:
        logging.info('Start consumer')
        consumer.start()
    finally:
        logging.info('Consumer stopped')
        consumer.stop()
