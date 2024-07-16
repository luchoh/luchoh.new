from typing import Optional
from pydantic import BaseModel
from .image import Image


class GalleryBase(BaseModel):
    title: str
    description: Optional[str] = None


class GalleryCreate(GalleryBase):
    pass


class GalleryUpdate(GalleryBase):
    title: Optional[str] = None


class Gallery(GalleryBase):
    id: int
    images: list[Image] = []

    class Config:
        orm_mode = True
