from pydantic import BaseModel

__all__ = (
    'SmsModel',
)


class SmsModel(BaseModel):
    user: str
    content: str
