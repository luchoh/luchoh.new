# Project: luchoh.com refactoring
# File: backend/app/schemas/image.py
from pydantic import BaseModel


class ImageBase(BaseModel):
    title: str
    description: str | None = None
    file_path: str


class ImageCreate(ImageBase):
    gallery_id: int


class Image(ImageBase):
    id: int
    gallery_id: int

    class Config:
        orm_mode = True
