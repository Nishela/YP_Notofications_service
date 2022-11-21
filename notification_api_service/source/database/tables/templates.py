from uuid import uuid4

from sqlalchemy import (
    Column,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base

__all__ = (
    'Templates',
)


class Templates(Base):
    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    body = Column(Text(), nullable=False)
    notification_id = Column(UUID(as_uuid=True), ForeignKey('notifications.id'))
    notification = relationship("Notifications", back_populates="template", uselist=False)
