# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/galleries.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Gallery)
def create_gallery(
    *,
    db: Session = Depends(deps.get_db),
    gallery_in: schemas.GalleryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    gallery = crud.gallery.create(db=db, obj_in=gallery_in)
    return gallery


@router.get("/", response_model=List[schemas.Gallery])
def read_galleries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
):
    galleries = crud.gallery.get_multi(db, skip=skip, limit=limit)
    return galleries


@router.get("/{gallery_id}", response_model=schemas.Gallery)
def read_gallery(
    gallery_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    gallery = crud.gallery.get(db, id=gallery_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return gallery


@router.put("/{gallery_id}", response_model=schemas.Gallery)
def update_gallery(
    *,
    db: Session = Depends(deps.get_db),
    gallery_id: int,
    gallery_in: schemas.GalleryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    gallery = crud.gallery.get(db, id=gallery_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    gallery = crud.gallery.update(db, db_obj=gallery, obj_in=gallery_in)
    return gallery


@router.delete("/{gallery_id}", response_model=schemas.Gallery)
def delete_gallery(
    *,
    db: Session = Depends(deps.get_db),
    gallery_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    gallery = crud.gallery.get(db, id=gallery_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    gallery = crud.gallery.remove(db, id=gallery_id)
    return gallery
