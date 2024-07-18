# Project: luchoh.com refactoring
# File: backend/app/models/gallery.py
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Association table for many-to-many relationship between Gallery and Image
gallery_image = Table('gallery_image', Base.metadata,
    Column('gallery_id', Integer, ForeignKey('galleries.id')),
    Column('image_id', Integer, ForeignKey('images.id'))
)

class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))

    images = relationship("Image", secondary=gallery_image, back_populates="galleries")