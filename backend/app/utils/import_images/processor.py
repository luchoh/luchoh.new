
import os
import shutil
import logging
from typing import List, Optional
from tqdm import tqdm
import click

from app.db.session import SessionLocal
from app.crud.image import image as image_crud
from app.schemas.image import ImageCreate
from app.core.config import settings
from app.utils.slugify import generate_slug

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_image_files(directory: str) -> List[str]:
    """Get image files from ONLY the specified directory (no recursion)."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp'}
    image_files = []
    
    try:
        # Only look at files in the current directory
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file() and os.path.splitext(entry.name)[1].lower() in image_extensions:
                    image_files.append(entry.path)
    except Exception as e:
        logger.error(f"Error scanning directory {directory}: {e}")
        return []
    
    return sorted(image_files)

def process_image(file_path: str, upload_dir: str) -> Optional[dict]:
    """Process a single image file."""
    try:
        # Get file info
        filename = os.path.basename(file_path)
        title = os.path.splitext(filename)[0]
        
        # Copy file to upload directory
        os.makedirs(upload_dir, exist_ok=True)
        new_path = os.path.join(upload_dir, filename)
        shutil.copy2(file_path, new_path)
        
        return {
            'title': title,
            'file_path': new_path
        }
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return None

def process_directory(directory: str, tags: tuple):
    """Process all images in a directory."""