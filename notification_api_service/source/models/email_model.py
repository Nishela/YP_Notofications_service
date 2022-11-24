from typing import List

from pydantic import BaseModel, EmailStr

from .model_mixins import DbManagerMixin

__all__ = (
    'EmailModel',
)


class EmailBody(BaseModel):
    title: str = ''
    text: str = ''


class EmailModel(BaseModel, DbManagerMixin):
    recipients: List[EmailStr]
    subject: str
    body: EmailBody
