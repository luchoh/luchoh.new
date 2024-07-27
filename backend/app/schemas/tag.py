# Project: luchoh.com refactoring
# File: backend/app/schemas/tag.py

from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = 0


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    name: Optional[str] = None


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True
