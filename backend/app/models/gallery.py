from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Gallery(Base):
    __tablename__ = "galleries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))

    images = relationship("Image", back_populates="gallery")
