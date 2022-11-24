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
    RABBIT_HOST: str = Field('localhost', env='RABBITMQ_HOST')
    RABBIT_PORT: int = Field(15672, env='RABBITMQ_PORT')
    RABBIT_USER: str = Field(..., env='RABBITMQ_USER')
    RABBIT_PASSWORD: str = Field(..., env='RABBITMQ_PASSWORD')


class MailConfig(BaseSettings):
    MAIL_USERNAME: str = Field(..., env='MAIL_USERNAME')
    MAIL_PASSWORD: str = Field(..., env='MAIL_PASSWORD')
    MAIL_PORT: int = Field(..., env='MAIL_PORT')
    MAIL_SERVER: str = Field(..., env='MAIL_SERVER')


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
