# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/images.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.image import image
from app.schemas import image as image_schema
from app.db.session import get_db
from app.auth.auth import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=image_schema.Image)
def create_image(
    image_in: image_schema.ImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return image.create(db=db, obj_in=image_in)


@router.get("/{image_id}", response_model=image_schema.Image)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = image.get(db=db, id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


# Add more endpoints for update, delete, list, etc.
