# Project: luchoh.com refactoring
# File: backend/app/crud/image.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.image import Image, Tag
from app.schemas.image import ImageCreate, ImageUpdate
from .base import CRUDBase
from app.utils.slugify import generate_slug
from app.core.config import settings


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def create(self, db: Session, *, obj_in: ImageCreate) -> Image:
        db_obj = Image(
            title=obj_in.title,
            description=obj_in.description,
            file_path=obj_in.file_path,
            thumbnail_url=obj_in.thumbnail_url,
            slug=generate_slug(obj_in.title),
        )
        db.add(db_obj)
        db.commit()

        # Handle tags
        for tag_name in obj_in.tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
            db_obj.tags.append(tag)

        # Handle sticky flag
        if obj_in.sticky:
            sticky_tag = db.query(Tag).filter(Tag.name == settings.DEFAULT_TAG).first()
            if not sticky_tag:
                sticky_tag = Tag(name=settings.DEFAULT_TAG)
                db.add(sticky_tag)
            db_obj.tags.append(sticky_tag)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Image, obj_in: ImageUpdate) -> Image:
        update_data = obj_in.dict(exclude_unset=True)

        # Handle tags separately
        tags = update_data.pop("tags", None)

        # Handle sticky separately
        sticky = update_data.pop(settings.DEFAULT_TAG, None)

        # Update slug if title is changed
        if "title" in update_data:
            update_data["slug"] = generate_slug(update_data["title"])

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        if tags is not None:
            db_obj.tags = []
            for tag_id in tags:
                tag = db.query(Tag).filter(Tag.id == tag_id).first()
                if tag:
                    db_obj.tags.append(tag)

        if sticky is not None:
            sticky_tag = db.query(Tag).filter(Tag.name == settings.DEFAULT_TAG).first()
            if not sticky_tag:
                sticky_tag = Tag(name=settings.DEFAULT_TAG)
                db.add(sticky_tag)

            if sticky and sticky_tag not in db_obj.tags:
                db_obj.tags.append(sticky_tag)
            elif not sticky and sticky_tag in db_obj.tags:
                db_obj.tags.remove(sticky_tag)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Image]:
        return (
            db.query(self.model)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_sticky_images(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Image]:
        return (
            db.query(self.model)
            .join(Image.tags)
            .filter(Tag.name == settings.DEFAULT_TAG)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tag_images_by_id(
        self, db: Session, *, tag_id: int, skip: int = 0, limit: int = 100
    ) -> List[Image]:
        return (
            db.query(self.model)
            .join(Image.tags)
            .filter(Tag.id == tag_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


image = CRUDImage(Image)
