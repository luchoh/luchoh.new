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
            name=obj_in.name, description=obj_in.description, order=obj_in.order
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_ordered(self, db: Session) -> List[Tag]:
        return db.query(Tag).order_by(Tag.order).all()


tag = CRUDTag(Tag)
