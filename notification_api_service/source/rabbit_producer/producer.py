from dataclasses import dataclass

from aio_pika import Message, DeliveryMode, ExchangeType
from core.config import get_settings
from .rabbit_utils import get_mq_connection

settings = get_settings()


@dataclass
class RabbitProducer:
    channel = None
    exchange_point = None

    async def async_configure(self, exchange_name='emails'):
        connection = await get_mq_connection()
        self.channel = await connection.channel()
        # await self.channel.set_qos(prefetch_count=1)
        self.exchange_point = await self.channel.declare_exchange(
            name=exchange_name,
            type=ExchangeType.DIRECT,
            durable=True
        )

        for queue_name in settings.queue_types.values():
            queue = await self.channel.declare_queue(queue_name, durable=True)
            await queue.bind(self.exchange_point)

        return self

    async def async_publish(self, routing_key, body):
        await self.exchange_point.publish(
                Message(body=body.encode(), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=routing_key,
            )
