# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/tags.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

from app.utils.image import get_full_url, generate_image_response

router = APIRouter()


@router.get("/", response_model=List[schemas.Tag])
def read_tags(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    tags = crud.tag.get_multi(db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=schemas.Tag)
def read_tag(
    tag_id: int,
    db: Session = Depends(deps.get_db),
):
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=schemas.Tag)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: schemas.TagCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    tag = crud.tag.create(db=db, obj_in=tag_in)
    return tag


@router.put("/{tag_id}", response_model=schemas.Tag)
def update_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: int,
    tag_in: schemas.TagUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    tag = crud.tag.update(db=db, db_obj=tag, obj_in=tag_in)
    return tag


@router.delete("/{tag_id}", response_model=schemas.Tag)
def delete_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    tag = crud.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    tag = crud.tag.remove(db=db, id=tag_id)
    return tag


@router.get("/{tag_id}/images")
async def get_images_by_tag(*, request: Request, db: Session = Depends(deps.get_db), tag_id: int):
    tag = crud.tag.get(db, id=tag_id)
    # tag = await Tag.get(name=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    images = crud.image.get_tag_images_by_id(db, tag_id=tag_id)
    return [generate_image_response(image, request) for image in images]
    # return images
