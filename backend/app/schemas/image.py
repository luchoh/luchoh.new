# Project: luchoh.com refactoring
# File: backend/app/schemas/image.py
from pydantic import BaseModel
from typing import Optional

class ImageBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str

class ImageCreate(ImageBase):
    gallery_id: int

class ImageUpdate(ImageBase):
    title: Optional[str] = None
    file_path: Optional[str] = None
    gallery_id: Optional[int] = None

class Image(ImageBase):
    id: int
    gallery_id: int

    class Config:
        from_attributes = True  # Updated from orm_mode = True