# Project: luchoh.com refactoring
# File: backend/app/crud/tag.py

"""CRUD operations for Tag model."""

from typing import List
from sqlalchemy.orm import Session
from app.models.image import Tag
from app.schemas.tag import TagCreate, TagUpdate
from .base import CRUDBase


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    """CRUD operations for Tag model."""

    def create(self, db: Session, obj_in: TagCreate) -> Tag:
        """
        Create a new tag.

        Args:
            db (Session): The database session.
            obj_in (TagCreate): The tag data to create.

        Returns:
            Tag: The created tag.
        """
        db_obj = Tag(
            name=obj_in.name,
            description=obj_in.description or "",
            order=obj_in.order or 0,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name(self, db: Session, name: str) -> Tag:
        """
        Get a tag by its name.

        Args:
            db (Session): The database session.
            name (str): The name of the tag to retrieve.

        Returns:
            Tag: The retrieved tag.
        """
        return db.query(Tag).filter(Tag.name == name).first()

    def get_all_ordered(self, db: Session) -> List[Tag]:
        """
        Get all tags ordered by their order attribute.

        Args:
            db (Session): The database session.

        Returns:
            List[Tag]: A list of all tags, ordered by their order attribute.
        """
        return db.query(Tag).order_by(Tag.order).all()


tag = CRUDTag(Tag)
