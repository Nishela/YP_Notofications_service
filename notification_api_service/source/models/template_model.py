from uuid import UUID, uuid4
from pydantic import BaseModel, Field

__all__ = (
    'TemplateModel',
)


class TemplateModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default='')
    body: str = Field(default='')
