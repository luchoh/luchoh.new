# Project: luchoh.com refactoring
# File: backend/app/crud/tag.py

from typing import List
from sqlalchemy.orm import Session
from app.models.image import Tag
from app.schemas.tag import TagCreate, TagUpdate
from .base import CRUDBase


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    def create(self, db: Session, *, obj_in: TagCreate) -> Tag:
        db_obj = Tag(
            name=obj_in.name,
            description=obj_in.description or "",
            order=obj_in.order or 0,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name(self, db: Session, *, name: str) -> Tag:
        return db.query(Tag).filter(Tag.name == name).first()

    def get_all_ordered(self, db: Session) -> List[Tag]:
        return db.query(Tag).order_by(Tag.order).all()

    def remove_invalid_tags(self, db: Session) -> None:
        invalid_tags = db.query(Tag).filter(Tag.name.in_(["1", ",", "9"])).all()
        for tag in invalid_tags:
            db.delete(tag)
        db.commit()


tag = CRUDTag(Tag)
