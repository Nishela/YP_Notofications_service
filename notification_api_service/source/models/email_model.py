from typing import List

from pydantic import BaseModel, EmailStr

from .model_utils.email_builder import EmailBuilder

__all__ = (
    'EmailModel',
)


class EmailBody(BaseModel):
    title: str = ''
    text: str = ''


class EmailModel(BaseModel):
    recipients: List[EmailStr]
    subject: str
    body: EmailBody

    class Config:
        builder = EmailBuilder
