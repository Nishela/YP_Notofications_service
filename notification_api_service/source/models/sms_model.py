from pydantic import BaseModel

from .model_mixins import DbManagerMixin

__all__ = (
    'SmsModel',
)


class SmsModel(BaseModel, DbManagerMixin):
    user: str
    content: str
