# Project: luchoh.com refactoring
# File: backend/app/schemas/user.py

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    username: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # This replaces orm_mode = True


class UserInDB(User):
    hashed_password: str
