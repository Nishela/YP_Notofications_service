import os
from functools import lru_cache
from logging import config as logging_config
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings, Field

from core.logger import LOGGING

__all__ = (
    'get_settings',
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
    MAIL_USERNAME: str = Field(..., env='MAIL_USERNAME')
    MAIL_PASSWORD: str = Field(..., env='MAIL_PASSWORD')
    MAIL_PORT: int = Field(..., env='MAIL_PORT')
    MAIL_SERVER: str = Field(..., env='MAIL_SERVER')
    TEMPLATE_FOLDER: Any = Field(os.path.join(BASE_DIR, 'source/html_templates'))


class Settings(BaseSettings):
    app = AppConfig()
    mail_config = MailConfig()


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()
