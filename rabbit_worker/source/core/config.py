import os
from functools import lru_cache
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from logger import LOGGING

load_dotenv()

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
    TEMPLATE_FOLDER: str = Field(os.path.join(BASE_DIR, 'source/html_templates'))


class QueueTypes(BaseSettings):
    NEW_REGISTRATION = 'new_registration'
    NOTIFICATION = 'notification'
    WEEKLY = 'weekly'


class Settings(BaseSettings):
    app = AppConfig()
    rabbitmq = RabbitMQ()
    mail_config = MailConfig()
    queue_types = QueueTypes().dict()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
