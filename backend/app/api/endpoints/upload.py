import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth.auth import get_current_active_user
from app.models.user import User
import uuid
import shutil

router = APIRouter()

# Use an absolute path for UPLOAD_DIRECTORY
UPLOAD_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads")
)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


def is_file_extension_allowed(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)
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
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}")

    file_size = os.path.getsize(file_location)

    return {
        "message": "File uploaded successfully",
        "original_filename": file.filename,
        "saved_filename": unique_filename,
        "file_path": file_location,
        "file_size": file_size,
        "upload_directory": UPLOAD_DIRECTORY,
    }
