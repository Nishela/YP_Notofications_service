from pydantic import BaseModel

from model_mixins import DbManagerMixin

__all__ = (
    'PushModel',
)


class PushModel(BaseModel, DbManagerMixin):
    user: str
    header: str
    content: str
