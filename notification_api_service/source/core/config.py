import os
from enum import Enum
from functools import lru_cache
from logging import config as logging_config
from typing import Any

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
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
    MAIL_FROM_NAME: str = Field(..., env='MAIL_FROM_NAME')
    MAIL_PASSWORD: str = Field(..., env='MAIL_PASSWORD')
    MAIL_PORT: int = Field(..., env='MAIL_PORT')
    MAIL_SERVER: str = Field(..., env='MAIL_SERVER')
    MAIL_SSL_TLS: bool = Field(True, env='MAIL_SSL_TLS')
    MAIL_STARTTLS: bool = Field(False, env='MAIL_STARTTLS')
    MAIL_USERNAME: str = Field(..., env='MAIL_USERNAME')
    TEMPLATE_FOLDER: Any = Field(os.path.join(BASE_DIR, 'source/html_templates'))
    VALIDATE_CERTS: bool = Field(False, env='VALIDATE_CERTS')


class RabbitConfig(BaseSettings):
    host: str = Field('localhost', env='RABBITMQ_HOST')
    port: int = Field(5672, env='RABBITMQ_PORT')
    login: str = Field(..., env='RABBITMQ_USER')
    password: str = Field(..., env='RABBITMQ_PASSWORD')


class QueueTypes(BaseSettings):
    NEW_REGISTRATION = 'new_registration'
    NOTIFICATION = 'notification'
    WEEKLY = 'weekly'


class Settings(BaseSettings):
    app = AppConfig()
    mail_config = ConnectionConfig(**MailConfig().dict())
    rabbit_config = RabbitConfig().dict()
    queue_types = QueueTypes().dict()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
