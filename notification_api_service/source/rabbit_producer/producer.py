from dataclasses import dataclass
from typing import Optional, Any

from aio_pika import Message, DeliveryMode, ExchangeType

from core.config import get_settings
from .rabbit_utils import get_mq_connection

settings = get_settings()


@dataclass
class RabbitProducer:
    # type[ignore]
    __channel = None
    __exchange_point = None

    async def async_configure(self, exchange_name: str):
        """
        Конфигурирование RabbitMQ.
        :param exchange_name: str
        :return:
        """

        connection = await get_mq_connection()
        self.__channel = await connection.channel()
        self.__exchange_point = await self.__channel.declare_exchange(
            name=exchange_name,
            type=ExchangeType.DIRECT,
            durable=True
        )

        for notification in settings.notification_types:
            queue = await self.__channel.declare_queue(notification.value, durable=True)
            await queue.bind(self.__exchange_point)

        return self

    async def async_publish(self, routing_key: str, body: str) -> None:
        """
        Добавление задачи в RabbitMQ
        :param routing_key: str
        :param body: str
        :return: None
        """

        await self.__exchange_point.publish(
            Message(body=body.encode('utf-8'), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )
