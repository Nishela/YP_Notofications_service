from pydantic import BaseModel

from .model_mixins import ManagerMixin

__all__ = (
    'SmsModel',
)


class SmsModel(BaseModel, ManagerMixin):
    user: str
    content: str
