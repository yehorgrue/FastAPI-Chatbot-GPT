from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# from beanie import PydanticObjectId
from uuid import UUID


class UserRegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr = None
    password: str

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class UserResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


############################


class UserPublicSchema(BaseModel):
    """
    Shared User properties. Visible to anyone.
    """

    # id: Optional[PydanticObjectId] = Field(..., alias="_id")
    uuid: UUID

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class UserPrivateSchema(UserPublicSchema):
    """
    Private User properties. Visible only to self and admins.
    """

    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = True

    phone: Optional[str]
    birthday: Optional[date] = None
    language: Optional[str]

    plan: Optional[str]
    haptic: bool = True
    dark_theme: bool = True

    provider: Optional[str] = None

    created_at: Optional[datetime] = None
    accessed_last: Optional[datetime] = None


    class Config:
        from_attributes = True
