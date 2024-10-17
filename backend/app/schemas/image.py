# Project: luchoh.com refactoring
# File: backend/app/schemas/image.py

"""Pydantic models for Image-related schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field
from .tag import Tag as TagSchema

# pylint: disable=too-few-public-methods

class ImageBase(BaseModel):
    """Base schema for Image with common attributes."""
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    file_path: str = Field(..., min_length=1)
    thumbnail_url: Optional[str] = None


class ImageCreate(ImageBase):
    """Schema for creating a new Image."""
    tags: List[str] = []
    sticky: bool = False


class ImageUpdate(BaseModel):
    """Schema for updating an existing Image."""
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[List[int]] = None
    sticky: Optional[bool] = None


class ImageInDBBase(ImageBase):
    """Base schema for Image with database attributes."""
    id: int
    tags: List[TagSchema] = []

    class Config:
        """Pydantic config for ORM mode."""
        from_attributes = True


class Image(ImageInDBBase):
    """Schema for Image response including slug and tags."""
    slug: str
    file_path: str
    thumbnail_url: Optional[str]
    tags: List[TagSchema] = []

    class Config:
        """Pydantic config for ORM mode."""
        orm_mode = True


class ImageInDB(ImageInDBBase):
    """Schema for Image as stored in the database."""


class CropData(BaseModel):
    """Schema for image cropping data."""
    x: float
    y: float
    width: float
    height: float
    rotate: float
    scaleX: float
    scaleY: float
