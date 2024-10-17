# Project: luchoh.com refactoring
# File: backend/app/crud/gallery.py

"""CRUD operations for Gallery model."""

from typing import List
from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate
from .base import CRUDBase


class CRUDGallery(CRUDBase[Image, ImageCreate, ImageUpdate]):
    """CRUD operations for Gallery model."""

    def create(self, db: Session, obj_in: ImageCreate) -> Image:
        """
        Create a new gallery.

        Args:
            db (Session): The database session.
            obj_in (ImageCreate): The gallery data to create.

        Returns:
            Image: The created gallery.
        """
        db_obj = Image(title=obj_in.title, description=obj_in.description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_images(
        self, db: Session, *, db_obj: Image, image_ids: List[int]
    ) -> Image:
        """
        Update the images associated with a gallery.

        Args:
            db (Session): The database session.
            db_obj (Image): The gallery to update.
            image_ids (List[int]): The list of image IDs to associate with the gallery.

        Returns:
            Image: The updated gallery.
        """
        images = db.query(Image).filter(Image.id.in_(image_ids)).all()
        db_obj.images = images
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


gallery = CRUDGallery(Image)
