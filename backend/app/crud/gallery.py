# Project: luchoh.com refactoring
# File: backend/app/crud/gallery.py
from typing import List
from sqlalchemy.orm import Session
from app.models.gallery import Gallery
from app.schemas.gallery import GalleryCreate, GalleryUpdate
from app.models.image import Image
from .base import CRUDBase


class CRUDGallery(CRUDBase[Gallery, GalleryCreate, GalleryUpdate]):
    def create(self, db: Session, *, obj_in: GalleryCreate) -> Gallery:
        db_obj = Gallery(title=obj_in.title, description=obj_in.description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_images(
        self, db: Session, *, db_obj: Gallery, image_ids: List[int]
    ) -> Gallery:
        images = db.query(Image).filter(Image.id.in_(image_ids)).all()
        db_obj.images = images
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


gallery = CRUDGallery(Gallery)
