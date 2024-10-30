# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/images.py
import logging
import os
from typing import List
from urllib.parse import unquote

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from PIL import Image as PILImage
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.db.session import get_db
from app.schemas.image import ImageCreate, ImageUpload
from app.utils.file import generate_file_path
from app.utils.image import generate_image_response
from app.utils.slugify import generate_slug
from app.utils.thumbnail import create_smart_thumbnail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Images module loaded")

router = APIRouter()


async def process_image_upload(file: UploadFile, image_data: ImageUpload, db: Session, current_user: models.User):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    relative_path, full_path = generate_file_path(file.filename)

    with open(full_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    tag_list = [tag.strip() for tag in image_data.tags.split(",") if tag.strip()]

    image_in = ImageCreate(
        title=image_data.title,
        description=image_data.description,
        file_path=relative_path,
        sticky=image_data.sticky,
        tags=tag_list,
    )

    return crud.image.create(db=db, obj_in=image_in)


@router.post("/", response_model=schemas.Image)
async def create_image(
    request: Request,
    file: UploadFile = File(...),
    image_data: ImageUpload = Depends(),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    logger.info("Create image endpoint called")

    try:
        image = await process_image_upload(file, image_data, db, current_user)

        # Generate thumbnail
        thumbnail_path = create_smart_thumbnail(image.file_path)

        # Update image with thumbnail information
        image = crud.image.update(db, db_obj=image, obj_in={"thumbnail_url": thumbnail_path})

        return generate_image_response(image, request)
    except Exception as e:
        logger.error("Error creating image: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{image_id_slug}", response_model=schemas.Image)
def read_image(
    image_id_slug: str,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        image_id = int(image_id_slug.split("-")[0])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid image ID") from exc

    image = crud.image.get(db=db, _id=image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    expected_slug = generate_slug(image.title)
    provided_slug = "-".join(image_id_slug.split("-")[1:])
    if provided_slug != expected_slug:
        raise HTTPException(status_code=404, detail="Image not found")

    response_data = generate_image_response(image, request)
    logger.info("Image response data: %s", response_data)
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
    image = crud.image.get(db=db, _id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if image_in.title:
        image_in.title = unquote(image_in.title)
    if image_in.description:
        image_in.description = unquote(image_in.description)

    if image_in.tags:
        image_in.tags = [int(tag_id) for tag_id in image_in.tags if str(tag_id).isdigit()]

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
    image = crud.image.get(db=db, _id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    image = crud.image.remove(db=db, _id=image_id)
    return generate_image_response(image, request)


@router.post("/{image_id}/thumbnail", response_model=schemas.Image)
async def create_thumbnail(
    image_id: int,
    crop_data: schemas.CropData,
    db: Session = Depends(deps.get_db),
):
    image = crud.image.get(db=db, _id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    with PILImage.open(image.file_path) as img:
        if crop_data.rotate != 0:
            img = img.rotate(-crop_data.rotate, expand=True)

        if crop_data.scaleX != 1 or crop_data.scaleY != 1:
            new_width = int(img.width * crop_data.scaleX)
            new_height = int(img.height * crop_data.scaleY)
            img = img.resize((new_width, new_height))

        cropped_img = img.crop((
            int(crop_data.x),
            int(crop_data.y),
            int(crop_data.x + crop_data.width),
            int(crop_data.y + crop_data.height),
        ))

        thumbnail_size = (200, 200)
        cropped_img.thumbnail(thumbnail_size)

        relative_thumbnail_path, full_thumbnail_path = generate_file_path(
            os.path.basename(image.file_path), prefix="thumbnail_"
        )
        cropped_img.save(full_thumbnail_path)

        image.thumbnail_url = relative_thumbnail_path
        db.add(image)
        db.commit()
        db.refresh(image)

    return image


@router.get("/by_tag/{tag_name}", response_model=List[schemas.Image])
def read_images_by_tag(
    request: Request,
    tag_name: str = settings.DEFAULT_TAG,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    tag = crud.tag.get_by_name(db, name=tag_name)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    images = crud.image.get_tag_images_by_id(db, tag_id=tag.id, skip=skip, limit=limit)
    return [generate_image_response(image, request) for image in images]
