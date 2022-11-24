import os
from enum import Enum
from functools import lru_cache
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from core.logger import LOGGING

__all__ = (
    'get_settings',
    'NotificationTypes',
)

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class AppConfig(BaseSettings):
    """
    Конфигурация приложения.
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field('PROJECT_NAME', env='PROJECT_NAME')
    logging = LOGGING


class MailConfig(BaseSettings):
    """
    Конфигурация email адреса проекта.
    """
    MAIL_FROM: str = Field(..., env='MAIL_USERNAME')


class RabbitConfig(BaseSettings):
    """
    Конфигурация RabbitMQ.
    """
    host: str = Field('localhost', env='RABBITMQ_HOST')
    port: int = Field(5672, env='RABBITMQ_PORT')
    login: str = Field(..., env='RABBITMQ_USER')
    password: str = Field(..., env='RABBITMQ_PASSWORD')
    EXCHANGE_POINT_NAME: str = Field('notifications', env='EXCHANGE_POINT_NAME')


class PostgresConfig(BaseSettings):
    """
    Конфигурация PostgreSQL.
    """
    SQLALCHEMY_DATABASE_URI: str = Field(..., env='SQLALCHEMY_DATABASE_URI')
    DB_ECHO_LOG: bool = Field(True, env='DB_ECHO_LOG')


class NotificationTypes(Enum):
    """
    Типы уведомлений.
    """
    EMAIL = 'email'
    PUSH = 'push'
    SMS = 'sms'


class Settings(BaseSettings):
    app = AppConfig()
    rabbit_config = RabbitConfig()
    notification_types = NotificationTypes
    mail_config = MailConfig()
    db_config = PostgresConfig()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
