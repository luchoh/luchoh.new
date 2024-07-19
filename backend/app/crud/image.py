# Project: luchoh.com refactoring
# File: backend/app/crud/image.py
from typing import List
from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate
from .base import CRUDBase


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def create_with_gallery(self, db: Session, obj_in: ImageCreate, gallery_id: int):
        db_obj = Image(
            title=obj_in.title,
            description=obj_in.description,
            file_path=obj_in.file_path,
            thumbnail_url=obj_in.thumbnail_url,
            gallery_id=gallery_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Image]:
        return db.query(self.model).offset(skip).limit(limit).all()


image = CRUDImage(Image)
