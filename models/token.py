from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer

from .base import Base


# SQLAlchemy Model
class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, unique=True, index=True, default=str(uuid4()))
    token_type = Column(String)


# Pydantic Model
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    uuid: Optional[UUID] = None
