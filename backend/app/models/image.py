# Project: luchoh.com refactoring
# File: backend/app/models/image.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
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
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    file_path = Column(String(255))
    thumbnail_url = Column(String(255), nullable=True)
    slug = Column(String(100), unique=True, index=True)
    sticky = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tags = relationship("Tag", secondary=image_tag, back_populates="images")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(500))
    order = Column(Integer, default=0)

    images = relationship("Image", secondary=image_tag, back_populates="tags")
