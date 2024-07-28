# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/images.py
import os
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from urllib.parse import unquote
from app.db.session import get_db
from app.auth.auth import get_current_active_user
from app.models.user import User
from app.utils.file import generate_file_path
from app.utils.slugify import generate_slug

from app.api import deps
from app import crud, models, schemas
from PIL import Image as PILImage

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Images module loaded")

router = APIRouter()


def get_full_url(request: Request, path: str) -> str:
    base_url = f"{request.base_url}"
    return f"{base_url}{path}"


def generate_image_response(image: models.Image, request: Request) -> dict:
    image_dict = image.__dict__.copy()
    image_dict["file_path"] = get_full_url(request, image.file_path)
    if image.thumbnail_url:
        image_dict["thumbnail_url"] = get_full_url(request, image.thumbnail_url)
    image_dict["tags"] = [schemas.Tag.from_orm(tag) for tag in image.tags]
    image_dict["slug"] = generate_slug(image.title)
    return image_dict


@router.post("/", response_model=schemas.Image)
async def create_image(
    request: Request,
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(None),
    sticky: bool = Form(False),
    tags: str = Form(""),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    logger.info("Create image endpoint called")

    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    relative_path, full_path = generate_file_path(file.filename)

    with open(full_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

    image_in = schemas.ImageCreate(
        title=title,
        description=description,
        file_path=relative_path,
        sticky=sticky,
        tags=tag_list,
    )

    try:
        image = crud.image.create(db=db, obj_in=image_in)
        return generate_image_response(image, request)
    except Exception as e:
        logger.error(f"Error creating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{image_id_slug}", response_model=schemas.Image)
def read_image(
    image_id_slug: str,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        image_id = int(image_id_slug.split("-")[0])
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid image ID")

    image = crud.image.get(db=db, id=image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Verify that the slug matches
    expected_slug = generate_slug(image.title)
    provided_slug = "-".join(image_id_slug.split("-")[1:])
    if provided_slug != expected_slug:
        raise HTTPException(status_code=404, detail="Image not found")

    response_data = generate_image_response(image, request)
    logger.info(f"Image response data: {response_data}")
    return response_data


@router.get("/", response_model=List[schemas.Image])
def read_images(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    images = crud.image.get_multi(db, skip=skip, limit=limit)
    return [generate_image_response(image, request) for image in images]


@router.put("/{image_id}", response_model=schemas.Image)
def update_image(
    *,
    db: Session = Depends(deps.get_db),
    image_id: int,
    image_in: schemas.ImageUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    request: Request,
):
    image = crud.image.get(db=db, id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Decode URL-encoded data
    if image_in.title:
        image_in.title = unquote(image_in.title)
    if image_in.description:
        image_in.description = unquote(image_in.description)

    # Ensure tags are a list of integers
    if image_in.tags:
        image_in.tags = [int(tag_id) for tag_id in image_in.tags if tag_id.isdigit()]

    image = crud.image.update(db=db, db_obj=image, obj_in=image_in)
    return generate_image_response(image, request)


@router.delete("/{image_id}", response_model=schemas.Image)
def delete_image(
    *,
    db: Session = Depends(deps.get_db),
    image_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    request: Request,
):
    image = crud.image.get(db=db, id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image = crud.image.remove(db=db, id=image_id)
    return generate_image_response(image, request)


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
        # Apply rotation if needed
        if crop_data.rotate != 0:
            img = img.rotate(-crop_data.rotate, expand=True)

        # Apply scaling if needed
        if crop_data.scaleX != 1 or crop_data.scaleY != 1:
            new_width = int(img.width * crop_data.scaleX)
            new_height = int(img.height * crop_data.scaleY)
            img = img.resize((new_width, new_height))

        # Crop the image
        cropped_img = img.crop(
            (
                int(crop_data.x),
                int(crop_data.y),
                int(crop_data.x + crop_data.width),
                int(crop_data.y + crop_data.height),
            )
        )

        # Resize to a square thumbnail
        thumbnail_size = (200, 200)  # You can adjust this size
        cropped_img.thumbnail(thumbnail_size)

        # Save the thumbnail
        relative_thumbnail_path, full_thumbnail_path = generate_file_path(
            os.path.basename(image.file_path), prefix="thumbnail_"
        )
        cropped_img.save(full_thumbnail_path)

        # Update the image record
        image.thumbnail_url = relative_thumbnail_path
        db.add(image)
        db.commit()
        db.refresh(image)

    return image


@router.get("/sticky", response_model=List[schemas.Image])
def read_sticky_images(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    images = crud.image.get_sticky_images(db, skip=skip, limit=limit)
    return [generate_image_response(image, request) for image in images]
