# Project: luchoh.com refactoring
# File: backend/app/crud/image.py
from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate
from .base import CRUDBase


class CRUDImage(CRUDBase[Image, ImageCreate, ImageCreate]):
    def create_with_gallery(self, db: Session, *, obj_in: ImageCreate, gallery_id: int) -> Image:
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


image = CRUDImage(Image)