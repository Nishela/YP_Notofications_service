# type: ignore
from enum import Enum
from typing import Callable, Optional

import pika
from pika import ConnectionParameters, PlainCredentials
from pika.adapters.select_connection import SelectConnection
from pika.channel import Channel
from pika.frame import Method
from pika.spec import BasicProperties, Basic

from decorators import backoff


class Consumer:
    def __init__(self, settings):
        __rabbit_credentials: PlainCredentials = PlainCredentials(
            settings.rabbitmq.RABBIT_USER,
            settings.rabbitmq.RABBIT_PASSWORD)
        self.pika_parameters: ConnectionParameters = pika.ConnectionParameters(
            host=settings.rabbitmq.RABBIT_HOST,
            port=settings.rabbitmq.RABBIT_PORT,
            credentials=__rabbit_credentials)
        self.queue_types: Enum = settings.notification_types
        self.channel: Optional[Channel] = None
        self.connection: Optional[SelectConnection] = None
        self.custom_callback: dict[str, Optional[Callable]] = {}

    def set_on_message_callback(self, callback_func: Callable, queue: str):
        self.custom_callback[queue] = callback_func

    def connect(self):
        connection = pika.SelectConnection(
            self.pika_parameters,
            on_open_callback=self.on_connected)
        self.connection = connection

    def on_connected(self, connection: SelectConnection):
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, new_channel: Channel):
        self.channel = new_channel
        for queue_type in self.queue_types:
            self.channel.queue_declare(
                queue=queue_type.value,
                durable=True,
                exclusive=False,
                auto_delete=False,
                callback=self.on_queue_declared
            )

    def on_queue_declared(self, method: Method):
        self.channel.basic_consume(method.method.queue, self.handle_delivery)

    def handle_delivery(self, channel: Channel, method: Basic.Deliver, header: BasicProperties, body: bytes):
        if callback := self.custom_callback.get(method.routing_key):
            if callback(channel, method, header, body):
                self.ack_message(method.delivery_tag)
            else:
                self.nack_message(method.delivery_tag)
        else:
            self.nack_message(method.delivery_tag, False)

    def ack_message(self, delivery_tag: int):
        self.channel.basic_ack(delivery_tag)

    def nack_message(self, delivery_tag: int, requeue: bool = True):
        self.channel.basic_nack(delivery_tag, requeue=requeue)

    @backoff()
    def start(self):
        self.connect()
        self.connection.ioloop.start()

    @backoff()
    def stop(self):
        self.connection.ioloop.stop()
        self.connection.close()
