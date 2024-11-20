
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import click
import hashlib
from app.core.config import settings

class FileHandler:
    """Handles file operations during image import."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.upload_dir = Path(settings.UPLOAD_DIRECTORY)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def handle_file(self, source_path: Path, exif_data: Dict) -> Optional[Path]:
        """Handle a single file during import."""
        try:
            file_hash = self._calculate_file_hash(source_path)
            if self._is_duplicate(file_hash):
                click.echo(f"Skipping duplicate file: {source_path}")
                return None

            dest_path = self._generate_destination_path(source_path, exif_data)
            
            if self.dry_run:
                click.echo(f"Would copy {source_path} to {dest_path}")
                return dest_path

            return self._copy_file(source_path, dest_path)

        except Exception as e:
            click.echo(f"Error handling file {source_path}: {e}", err=True)
            return None

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _is_duplicate(self, file_hash: str) -> bool:
        """Check if a file with this hash already exists."""
        # This should be implemented to check against your database
        return False

    def _generate_destination_path(self, source_path: Path, exif_data: Dict) -> Path:
        """Generate destination path based on file and EXIF data."""
        date_taken = self._get_date_from_exif(exif_data)
        year = date_taken.strftime('%Y')
        month = date_taken.strftime('%m')
        
        dest_dir = self.upload_dir / year / month
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        return dest_dir / source_path.name

    def _copy_file(self, source_path: Path, dest_path: Path) -> Path:
        """Copy file to destination, ensuring uniqueness."""
        if dest_path.exists():
            base = dest_path.stem
            counter = 1
            while dest_path.exists():
                dest_path = dest_path.with_name(f"{base}_{counter}{dest_path.suffix}")
                counter += 1

        shutil.copy2(source_path, dest_path)
        return dest_path

    def _get_date_from_exif(self, exif_data: Dict) -> datetime:
        """Extract date from EXIF data or use current date."""