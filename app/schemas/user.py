from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
