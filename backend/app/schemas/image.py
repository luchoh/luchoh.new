# Project: luchoh.com refactoring
# File: backend/app/schemas/image.py
from typing import Optional
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    file_path: str = Field(..., min_length=1)
    thumbnail_url: Optional[str] = None


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    # thumbnail_url: Optional[str] = None


class ImageInDBBase(ImageBase):
    id: int

    class Config:
        from_attributes = True


class Image(ImageInDBBase):
    pass


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
