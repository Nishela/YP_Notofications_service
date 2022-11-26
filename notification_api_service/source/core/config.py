import os
from enum import Enum
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

__all__ = (
    'get_settings',
    'NotificationTypes',
)

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class AppConfig(BaseSettings):
    """
    Конфигурация приложения.
    """
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str
    logging = LOGGING

    class Config:
        env_prefix = 'glob_'
        case_sensitive = False


class MailConfig(BaseSettings):
    """
    Конфигурация email адреса проекта.
    """
    mail_from: str

    class Config:
        env_prefix = 'smtp_'
        case_sensitive = False


class RabbitConfig(BaseSettings):
    """
    Конфигурация RabbitMQ.
    """
    host: str
    port: int
    login: str
    password: str
    exchange_point_name: str

    # uri: str

    class Config:
        env_prefix = 'rabbitmq_'
        case_sensitive = False


class PostgresConfig(BaseSettings):
    """
    Конфигурация PostgreSQL.
    """
    database_uri: str
    db_echo_log: bool

    class Config:
        env_prefix = 'sqlalchemy_'
        case_sensitive = False


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
