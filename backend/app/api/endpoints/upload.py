import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.auth.auth import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # TODO: Implement proper file storage (e.g., to a cloud service)
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return {"filename": file.filename}
