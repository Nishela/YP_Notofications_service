from typing import List

from pydantic import BaseModel, EmailStr

from .model_mixins import ManagerMixin

__all__ = (
    'EmailModel',
)


class EmailBody(BaseModel):
    title: str = ''
    text: str = ''


class EmailModel(BaseModel, ManagerMixin):
    recipients: List[EmailStr]
    subject: str
    body: EmailBody
