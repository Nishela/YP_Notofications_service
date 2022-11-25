import os
from enum import Enum
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))


class AppConfig(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_name: str = Field('PROJECT_NAME', env='PROJECT_NAME')
    logging = LOGGING


class RabbitMQ(BaseSettings):
    host: str = 'localhost'
    port: int = 15672
    login: str = ...
    password: str = ...

    class Config:
        env_prefix = 'rabbitmq_'


class MailConfig(BaseSettings):
    username: str = ...
    password: str = ...
    port: int = ...
    server: str = ...

    class Config:
        env_prefix = 'mail_'


class NotificationTypes(Enum):
    """
    Типы уведомлений.
    """
    EMAIL = 'email'
    PUSH = 'push'
    SMS = 'sms'


class Settings(BaseSettings):
    app = AppConfig()
    rabbitmq = RabbitMQ()
    mail_config = MailConfig()
    notification_types = NotificationTypes


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
