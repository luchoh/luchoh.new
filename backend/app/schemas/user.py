# Project: luchoh.com refactoring
# File: backend/app/schemas/user.py

"""Pydantic models for User-related schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr

# pylint: disable=too-few-public-methods

class UserBase(BaseModel):
    """Base schema for User with common attributes."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    username: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new User."""
    email: EmailStr
    password: str
    username: str


class UserUpdate(UserBase):
    """Schema for updating an existing User."""
    password: Optional[str] = None


class User(UserBase):
    """Schema for User response."""
    id: int
    is_active: bool
    username: str
    email: EmailStr

    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True  # This replaces orm_mode = True


class UserInDB(User):
    """Schema for User as stored in the database."""
    hashed_password: str
