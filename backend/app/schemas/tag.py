# Project: luchoh.com refactoring
# File: backend/app/schemas/tag.py

"""Pydantic models for Tag-related schemas."""

from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods

class TagBase(BaseModel):
    """Base schema for Tag with common attributes."""
    name: str
    description: Optional[str] = None
    order: Optional[int] = 0


class TagCreate(TagBase):
    """Schema for creating a new Tag."""


class TagUpdate(TagBase):
    """Schema for updating an existing Tag."""
    name: Optional[str] = None


class Tag(TagBase):
    """Schema for Tag response including id."""
    id: int

    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True
