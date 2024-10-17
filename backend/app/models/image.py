# Project: luchoh.com refactoring
# File: backend/app/models/image.py
# pylint: disable=too-few-public-methods
# pylint: disable=not-callable


"""SQLAlchemy models for Image and Tag."""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

image_tag = Table(
    "image_tag",
    Base.metadata,
    Column("image_id", Integer, ForeignKey("images.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Image(Base):
    """
    SQLAlchemy model for the Image table.

    Attributes:
        id (int): Primary key for the image.
        title (str): Title of the image.
        description (str): Description of the image.
        file_path (str): Path to the image file.
        thumbnail_url (str): URL of the image thumbnail.
        created_at (datetime): Timestamp of when the image was created.
        updated_at (datetime): Timestamp of when the image was last updated.
        tags (relationship): Many-to-many relationship with Tag model.
    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    file_path = Column(String(255))
    thumbnail_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tags = relationship("Tag", secondary=image_tag, back_populates="images")


class Tag(Base):
    """
    SQLAlchemy model for the Tag table.

    Attributes:
        id (int): Primary key for the tag.
        name (str): Name of the tag.
        description (str): Description of the tag.
        order (int): Order of the tag for sorting purposes.
        images (relationship): Many-to-many relationship with Image model.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(500))
    order = Column(Integer, default=0)

    images = relationship("Image", secondary=image_tag, back_populates="tags")
