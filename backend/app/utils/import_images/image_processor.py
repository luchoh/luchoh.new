
from pathlib import Path
from typing import Set
import click
from tqdm import tqdm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.image import image as crud_image
from app.schemas.image import ImageCreate
from app.utils.slugify import generate_slug
from .file_handler import FileHandler
from .exif_reader import ExifReader

class ImageProcessor:
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler
        self.exif_reader = ExifReader()
        self.processed_files: Set[str] = set()
        self.db: Session = SessionLocal()

    def __del__(self):
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def process_directory(self, directory: Path, recursive: bool = True) -> None:
        pattern = '**/*' if recursive else '*'
        files = list(directory.glob(pattern))
        
        with tqdm(total=len(files), desc="Processing files") as pbar:
            for file_path in files:
                if self._should_process_file(file_path):
                    try:
                        self._process_single_file(file_path)
                    except Exception as e:
                        click.echo(f"Error processing {file_path}: {e}", err=True)
                pbar.update(1)

    def _should_process_file(self, file_path: Path) -> bool:
        """
        Determine if a file should be processed.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            bool: True if the file should be processed, False otherwise
        """
        if not file_path.is_file():
            return False
            
        if file_path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.gif'}:
            return False
            
        if str(file_path) in self.processed_files:
            return False
            
        return True

    def _process_single_file(self, file_path: Path) -> None:
        if not self._should_process_file(file_path):
            return

        try:
            exif_data = self.exif_reader.read_exif(file_path)
            dest_path = self.file_handler.handle_file(file_path, exif_data)
            
            if dest_path:
                title = file_path.stem
                image_create = ImageCreate(
                    title=title,
                    description=exif_data.get('description', ''),
                    file_path=str(dest_path.relative_to(self.file_handler.upload_dir)),
                    tags=[]
                )
                
                slug = generate_slug(title)
                crud_image.create(self.db, obj_in=image_create, slug=slug)
                self.processed_files.add(str(file_path))
                click.echo(f"Successfully processed: {file_path}")
            
        except Exception as e:
            click.echo(f"Error processing {file_path}: {e}", err=True)
            raise