from dataclasses import dataclass

from aio_pika import Message, DeliveryMode, ExchangeType
from core.config import get_settings
from .rabbit_utils import get_mq_connection

settings = get_settings()


@dataclass
class RabbitProducer:
    __channel = None
    __exchange_point = None

    async def async_configure(self, exchange_name):
        connection = await get_mq_connection()
        self.__channel = await connection.channel()
        self.__exchange_point = await self.__channel.declare_exchange(
            name=exchange_name,
            type=ExchangeType.DIRECT,
            durable=True
        )

        for queue_name in settings.queue_types.values():
            queue = await self.__channel.declare_queue(queue_name, durable=True)
            await queue.bind(self.__exchange_point)

        return self

    async def async_publish(self, routing_key, body):
        await self.__exchange_point.publish(
            Message(body=body.encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )
