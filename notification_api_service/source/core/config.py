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
    mail_from: str = Field(..., env='MAIL_USERNAME')


class RabbitConfig(BaseSettings):
    """
    Конфигурация RabbitMQ.
    """
    host: str = 'localhost'
    port: int = 5672
    login: str = ...
    password: str = ...
    exchange_point_name: str = 'notifications'

    class Config:
        env_prefix = 'rabbitmq_'


class PostgresConfig(BaseSettings):
    """
    Конфигурация PostgreSQL.
    """
    uri: str = ...
    echo_log: bool = True

    class Config:
        env_prefix = 'postgres_'


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
