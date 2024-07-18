# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/galleries.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.gallery import gallery
from app.schemas import gallery as gallery_schema
from app.db.session import get_db
from app.auth.auth import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=gallery_schema.Gallery)
def create_gallery(
    gallery_in: gallery_schema.GalleryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_gallery = gallery.get_by_title(db, title=gallery_in.title)
    if db_gallery:
        raise HTTPException(
            status_code=400, detail="A gallery with this title already exists."
        )
    return db_gallery.create(db=db, obj_in=gallery_in)


@router.get("/", response_model=List[gallery_schema.Gallery])
def read_galleries(
    db: Session = Depends(get_db),
    # , current_user: User = Depends(get_current_active_user)
):
    print("Accessing /galleries/ endpoint")
    return gallery.get_multi(db)


@router.get("/{gallery_id}", response_model=gallery_schema.Gallery)
def read_gallery(gallery_id: int, db: Session = Depends(get_db)):
    db_gallery = gallery.get(db, id=gallery_id)
    if db_gallery is None:
        raise HTTPException(status_code=404, detail="Gallery not found")
    return db_gallery


@router.put("/{gallery_id}", response_model=gallery_schema.Gallery)
def update_gallery(
    gallery_id: int,
    gallery_in: gallery_schema.GalleryUpdate,
    db: Session = Depends(get_db),
):
    db_gallery = gallery.get(db, id=gallery_id)
    if db_gallery is None:
        raise HTTPException(status_code=404, detail="Gallery not found")
    db_gallery = gallery.update(db=db, db_obj=gallery, obj_in=gallery_in)
    return db_gallery


@router.delete("/{gallery_id}", response_model=gallery_schema.Gallery)
def delete_gallery(gallery_id: int, db: Session = Depends(get_db)):
    db_gallery = gallery.get(db, id=gallery_id)
    if db_gallery is None:
        raise HTTPException(status_code=404, detail="Gallery not found")
    db_gallery = gallery.remove(db=db, id=gallery_id)
    return db_gallery
