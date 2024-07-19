# Project: luchoh.com refactoring
# File: backend/app/crud/gallery.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.gallery import Gallery
from app.schemas.gallery import GalleryCreate, GalleryUpdate
from app.models.image import Image
from .base import CRUDBase


class CRUDGallery(CRUDBase[Gallery, GalleryCreate, GalleryUpdate]):
    def create_with_images(
        self,
        db: Session,
        *,
        obj_in: GalleryCreate,
        image_ids: Optional[List[int]] = None,
    ) -> Gallery:
        db_obj = Gallery(title=obj_in.title, description=obj_in.description)
        images = db.query(Image).filter(Image.id.in_(image_ids)).all()
        db_obj.images = images
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_images(
        self, db: Session, *, db_obj: Gallery, image_ids: List[int]
    ) -> Gallery:
        if image_ids:
            images = db.query(Image).filter(Image.id.in_(image_ids)).all()
            db_obj.images = images
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


gallery = CRUDGallery(Gallery)
