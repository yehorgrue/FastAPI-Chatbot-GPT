from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from datetime import datetime
from uuid import uuid4


from models.base import Base

from models.subscription import Subscription

from models.role import Role

import uuid


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)

    # Constraints like min_length and max_length can be enforced at the application level
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    hashed_password = Column(String, nullable=False)

    # Additional fields
    phone = Column(String)
    birthday = Column(Date)
    language = Column(String)
    avatar = Column(String)
    plan = Column(String)
    # haptic = Column(Boolean, default=False)
    dark_theme = Column(Boolean, default=False)
    provider = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    accessed_last = Column(DateTime, default=datetime.now)

    is_active = Column(Boolean, default=True)

    disabled: bool | None = False
    subscription: Subscription

    role: Role

    # thread_id = Column(String)

    messages: relationship("Messages")

    class Config:
        from_attributes = True


class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String)
    message = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    sentAt = Column(DateTime, default=datetime.now)

    class Config:
        from_attributes = True
