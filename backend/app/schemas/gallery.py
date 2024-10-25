# Project: luchoh.com refactoring
# File: backend/app/schemas/gallery.py

from typing import List, Optional
from pydantic import BaseModel
from .image import Image


class GalleryBase(BaseModel):
    title: str
    description: Optional[str] = None


class GalleryCreate(GalleryBase):
    pass


class GalleryUpdate(GalleryBase):
    pass


class Gallery(GalleryBase):
    id: int
    images: List[Image] = []

    class Config:
        orm_mode = True
