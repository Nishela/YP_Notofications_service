from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base import Base

__all__ = (
    'Notifications',
)


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(256), unique=True, nullable=False)
    template = relationship("Templates", back_populates="notification", uselist=False)
