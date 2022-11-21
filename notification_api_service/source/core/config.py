import os
from functools import lru_cache
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from core.logger import LOGGING

__all__ = (
    'get_settings',
    'QueueTypes',
)

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class AppConfig(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field('PROJECT_NAME', env='PROJECT_NAME')
    logging = LOGGING


class MailConfig(BaseSettings):
    MAIL_FROM: str = Field(..., env='MAIL_USERNAME')


class RabbitConfig(BaseSettings):
    host: str = Field('localhost', env='RABBITMQ_HOST')
    port: int = Field(5672, env='RABBITMQ_PORT')
    login: str = Field(..., env='RABBITMQ_USER')
    password: str = Field(..., env='RABBITMQ_PASSWORD')
    EXCHANGE_POINT_NAME: str = Field('emails', env='EXCHANGE_POINT_NAME')


class PostgresConfig(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = Field(..., env='SQLALCHEMY_DATABASE_URI')
    DB_ECHO_LOG: bool = Field(True, env='DB_ECHO_LOG')


class QueueTypes(BaseSettings):
    NEW_REGISTRATION = 'new_registration'
    NOTIFICATION = 'notification'
    WEEKLY = 'weekly'


class Settings(BaseSettings):
    app = AppConfig()
    rabbit_config = RabbitConfig()
    queue_types = QueueTypes().dict()
    mail_config = MailConfig()
    db_config = PostgresConfig()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
