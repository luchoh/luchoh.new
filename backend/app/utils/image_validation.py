
from PIL import Image
from pathlib import Path
from typing import Optional

def validate_image(file_path: Path) -> Optional[str]:
    """
    Validate image file integrity.
    Returns error message if invalid, None if valid.
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return None
    except Exception as e:
        return str(e)

def get_image_dimensions(file_path: Path) -> tuple:
    """Get image dimensions."""
    with Image.open(file_path) as img:
        return img.size

def check_minimum_size(file_path: Path, min_width: int = 800, min_height: int = 600) -> bool:
    """Check if image meets minimum size requirements.