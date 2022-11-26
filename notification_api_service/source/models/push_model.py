from pydantic import BaseModel

from .model_mixins import ManagerMixin

__all__ = (
    'PushModel',
)


class PushModel(BaseModel, ManagerMixin):
    user: str
    header: str
    content: str
