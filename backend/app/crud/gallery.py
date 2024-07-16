from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.gallery import Gallery
from app.schemas.gallery import GalleryCreate, GalleryUpdate


class CRUDGallery(CRUDBase):
    def create(self, db: Session, *, obj_in: GalleryCreate) -> Gallery:
        db_obj = Gallery(title=obj_in.title, description=obj_in.description)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_title(self, db: Session, *, title: str) -> Gallery:
        return db.query(Gallery).filter(Gallery.title == title).first()

    def update(self, db: Session, *, db_obj: Gallery, obj_in: GalleryUpdate) -> Gallery:
        update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


gallery = CRUDGallery(Gallery)
