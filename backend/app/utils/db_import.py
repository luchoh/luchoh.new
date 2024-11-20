
from pathlib import Path
from sqlalchemy.orm import Session
from app.crud.image import image as image_crud
from app.schemas.image import ImageCreate
from app.utils.slugify import generate_slug

def import_to_database(
    db: Session,
    file_path: Path,
    title: str,
    description: str = "",
    tags: list = None
) -> None:
    """Import image information to database.