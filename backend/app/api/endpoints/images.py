# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/images.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.image import image
from app.schemas.image import Image as ImageSchema, ImageCreate
from app.db.session import get_db
from app.auth.auth import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ImageSchema)
def create_image(
    image_in: ImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return image.create(db=db, obj_in=image_in)


@router.get("/{image_id}", response_model=ImageSchema)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = image.get(db=db, id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.get("/", response_model=List[ImageSchema])
def read_images(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    images = image.get_multi(db, skip=skip, limit=limit)
    return [ImageSchema.from_orm(img) for img in images]


# Add more endpoints for update, delete, etc. if needed
