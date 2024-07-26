# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/images.py
import os
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.auth.auth import get_current_active_user
from app.models.user import User
from app.api import deps
from app import crud, models, schemas
from PIL import Image as PILImage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Images module loaded")

router = APIRouter()


def get_full_url(request: Request, path: str) -> str:
    base_url = f"{request.base_url}"
    return f"{base_url}{path}"


@router.post("/", response_model=schemas.Image)
async def create_image(
    image_in: schemas.ImageCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    logger.info("Create image endpoint called")
    logger.info(f"Received image data: {image_in.dict()}")

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    try:
        image = crud.image.create(db=db, obj_in=image_in)
        return image
    except Exception as e:
        logger.error(f"Error creating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{image_id}", response_model=schemas.Image)
def read_image(
    image_id: int,
    request: Request,
    db: Session = Depends(deps.get_db),
):
    image = crud.image.get(db=db, id=image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    image_dict = image.__dict__
    image_dict["file_path"] = get_full_url(request, image.file_path)
    if image.thumbnail_url:
        image_dict["thumbnail_url"] = get_full_url(request, image.thumbnail_url)
    return image_dict


@router.get("/", response_model=List[schemas.Image])
def read_images(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    images = crud.image.get_multi(db, skip=skip, limit=limit)
    for image in images:
        image.file_path = get_full_url(request, image.file_path)
        if image.thumbnail_url:
            image.thumbnail_url = get_full_url(request, image.thumbnail_url)
    return images


@router.put("/{image_id}", response_model=schemas.Image)
def update_image(
    *,
    db: Session = Depends(deps.get_db),
    image_id: int,
    image_in: schemas.ImageUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    image = crud.image.get(db=db, id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image = crud.image.update(db=db, db_obj=image, obj_in=image_in)
    return image


@router.delete("/{image_id}", response_model=schemas.Image)
def delete_image(
    *,
    db: Session = Depends(deps.get_db),
    image_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    image = crud.image.get(db=db, id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image = crud.image.remove(db=db, id=image_id)
    return image


@router.post("/{image_id}/thumbnail", response_model=schemas.Image)
async def create_thumbnail(
    image_id: int,
    crop_data: schemas.CropData,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    image = crud.image.get(db=db, id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Open the image
    with PILImage.open(image.file_path) as img:
        # Crop the image
        cropped_img = img.crop(
            (
                crop_data.x,
                crop_data.y,
                crop_data.x + crop_data.width,
                crop_data.y + crop_data.height,
            )
        )

        # Resize to a square thumbnail
        thumbnail_size = (200, 200)  # You can adjust this size
        cropped_img.thumbnail(thumbnail_size)

        # Save the thumbnail
        thumbnail_path = f"/thumbnails/{os.path.basename(image.file_path)}"
        full_thumbnail_path = os.path.join(settings.UPLOAD_DIRECTORY, thumbnail_path)
        os.makedirs(os.path.dirname(full_thumbnail_path), exist_ok=True)
        cropped_img.save(full_thumbnail_path)

        # Update the image record
        image.thumbnail_url = thumbnail_path
        db.commit()

    return image
