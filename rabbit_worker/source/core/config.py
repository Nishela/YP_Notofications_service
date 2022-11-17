import os
import pika
from dotenv import load_dotenv
from pika import ConnectionParameters, PlainCredentials

load_dotenv()


class Config:
    _rabbit_host: str = os.getenv('RABBITMQ_HOST', 'localhost')
    _rabbit_port: int = int(os.getenv('RABBITMQ_PORT', 15672))
    _rabbit_user: str = os.getenv('RABBITMQ_USER')
    _rabbit_password: str = os.getenv('RABBITMQ_PASS')
    _rabbit_credentials: PlainCredentials = PlainCredentials(_rabbit_user, _rabbit_password)
    pika_parameters: ConnectionParameters = pika.ConnectionParameters(host=_rabbit_host, port=_rabbit_port,
                                                                      credentials=_rabbit_credentials)
