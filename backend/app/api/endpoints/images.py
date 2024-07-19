# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/images.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header, Form
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime
from app.crud.image import image
from app.schemas import image as image_schema
from app.db.session import get_db
from app.auth.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

# Use an absolute path for UPLOAD_DIRECTORY
UPLOAD_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads")
)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


def is_file_extension_allowed(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/upload/", response_model=image_schema.Image)
async def upload_image(
    file: UploadFile = File(...),
    name: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    authorization: str = Header(None),
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not is_file_extension_allowed(file.filename):
        raise HTTPException(status_code=400, detail="File extension not allowed")

    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Generate a unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")

    # Create image record in database
    image_in = image_schema.ImageCreate(
        title=title,
        description=description,
        file_path=file_location,
        thumbnail_url=None,
    )
    db_image = image.create(db=db, obj_in=image_in)

    # Convert the SQLAlchemy model to a Pydantic model
    return image_schema.Image.model_validate(db_image)


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
