# Project: luchoh.com refactoring
# File: backend/app/schemas/image.py

from typing import List, Optional
from pydantic import BaseModel, Field
from .tag import Tag as TagSchema


class ImageBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    file_path: str = Field(..., min_length=1)
    thumbnail_url: Optional[str] = None
    sticky: Optional[bool] = False


class ImageCreate(ImageBase):
    tags: List[str] = []


class ImageUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = None
    sticky: Optional[bool] = None


class ImageInDBBase(ImageBase):
    id: int
    tags: List[TagSchema] = []

    class Config:
        from_attributes = True


class Image(ImageInDBBase):
    slug: str
    file_path: str
    thumbnail_url: Optional[str]
    tags: List[TagSchema] = []

    class Config:
        orm_mode = True


class ImageInDB(ImageInDBBase):
    pass


class CropData(BaseModel):
    x: float
    y: float
    width: float
    height: float
    rotate: float
    scaleX: float
    scaleY: float
