from app.models.image import Image
from app.schemas.image import ImageCreate
from .base import CRUDBase


class CRUDImage(CRUDBase):
    def create_with_gallery(self, db, obj_in: ImageCreate, gallery_id: int):
        db_obj = Image(
            title=obj_in.title,
            description=obj_in.description,
            file_path=obj_in.file_path,
            gallery_id=gallery_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


image = CRUDImage(Image)
