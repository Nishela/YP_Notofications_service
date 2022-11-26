from pydantic import BaseModel

__all__ = (
    'PushModel',
)


class PushModel(BaseModel):
    user: str
    header: str
    content: str
