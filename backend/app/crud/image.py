# Project: luchoh.com refactoring
# File: backend/app/crud/image.py

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.image import Image, Tag
from app.schemas.image import ImageCreate, ImageUpdate
from .base import CRUDBase
from app.utils.slugify import generate_slug


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def create(self, db: Session, *, obj_in: ImageCreate) -> Image:
        db_obj = Image(
            title=obj_in.title,
            description=obj_in.description,
            file_path=obj_in.file_path,
            thumbnail_url=obj_in.thumbnail_url,
            slug=obj_in.slug or generate_slug(obj_in.title),
            sticky=obj_in.sticky if obj_in.sticky is not None else False,
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

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Image, obj_in: ImageUpdate) -> Image:
        update_data = obj_in.dict(exclude_unset=True)
        if "title" in update_data and not update_data.get("slug"):
            update_data["slug"] = generate_slug(update_data["title"])

        # Handle tags separately
        tags = update_data.pop("tags", None)

        for field in update_data:
            setattr(db_obj, field, update_data[field])

        if tags is not None:
            db_obj.tags.clear()
            for tag_id in tags:
                tag = db.query(Tag).filter(Tag.id == int(tag_id)).first()
                if tag:
                    db_obj.tags.append(tag)

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
            .filter(self.model.sticky == True)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tag_images_by_id(
        self, db: Session, *, tag_id, skip: int = 0, limit: int = 100
    ) -> List[Image]:
        return (
            db.query(self.model)
            .join(Image.tags)
            .filter(Tag.id == int(tag_id))
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        # images_with_tag = session.query(Image).join(Image.tags).filter(Tag.id == tag_id).all()


image = CRUDImage(Image)
