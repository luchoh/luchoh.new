# Project: luchoh.com refactoring
# File: backend/app/schemas/image.py
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ImageBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    thumbnail_url: Optional[str] = None


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class ImageInDBBase(ImageBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Image(ImageInDBBase):
    pass


class ImageInDB(ImageInDBBase):
    pass
