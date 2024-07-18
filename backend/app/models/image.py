# Project: luchoh.com refactoring
# File: backend/app/models/image.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    file_path = Column(String(255))
    gallery_id = Column(Integer, ForeignKey("galleries.id"))

    gallery = relationship("Gallery", back_populates="images")
