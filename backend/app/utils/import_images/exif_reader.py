"""EXIF data reading functionality for importing images."""

import os
from pathlib import Path
from typing import Dict, Any
import exifread
import click
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

class ExifReader:
    """Handles reading EXIF data from image files."""

    def read_exif(self, file_path: Path) -> Dict[str, Any]:
        """Read EXIF data from an image file."""
        try:
            with Image.open(file_path) as img:
                exif = {}
                if hasattr(img, '_getexif'):  # Check if image has EXIF data
                    img_exif = img._getexif()
                    if img_exif:
                        for tag_id, value in img_exif.items():
                            tag = TAGS.get(tag_id, tag_id)
                            exif[tag] = str(value)

                # Add basic image info
                exif['ImageWidth'] = img.width
                exif['ImageHeight'] = img.height
                exif['Format'] = img.format
                exif['Mode'] = img.mode

                # Add file info
                file_stats = os.stat(file_path)
                exif['FileSize'] = file_stats.st_size
                exif['FileModifyDate'] = datetime.fromtimestamp(
                    file_stats.st_mtime
                ).strftime('%Y:%m:%d %H:%M:%S')

                return self._process_tags(exif)

        except Exception as e:
            click.echo(f"Error reading EXIF from {file_path}: {e}", err=True)
            return {}

    def _process_tags(self, tags: Dict) -> Dict[str, Any]:
        """Process raw EXIF tags into a clean dictionary."""
        processed = {}
        
        # Map of common EXIF tags to process
        tag_mapping = {
            'DateTimeOriginal': 'DateTimeOriginal',
            'Make': 'Make',
            'Model': 'Model',
            'ExposureTime': 'ExposureTime',
            'FNumber': 'FNumber',
            'ISOSpeedRatings': 'ISO',
            'FocalLength': 'FocalLength',
            'LensModel': 'LensModel',
            'ImageWidth': 'Width',
            'ImageHeight': 'Height',
            'FileSize': 'FileSize',
            'FileModifyDate': 'ModifyDate'
        }

        # Process each tag according to the mapping
        for exif_tag, output_tag in tag_mapping.items():
            if exif_tag in tags:
                processed[output_tag] = str(tags[exif_tag])

        # Add image description if available
        if 'ImageDescription' in tags:
            processed['description'] = str(tags['ImageDescription'])
        
        # If no DateTimeOriginal, use file modify date
        if 'DateTimeOriginal' not in processed and 'ModifyDate' in processed:
            processed['DateTimeOriginal'] = processed['ModifyDate']

        return processed

    def get_date_taken(self, exif_data: Dict[str, Any]) -> datetime:
        """Extract the date when the image was taken from EXIF data."""
        date_str = exif_data.get('DateTimeOriginal')
        if date_str:
            try:
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
            except ValueError:
                pass
        
        # Fallback to file modification date
        modify_date = exif_data.get('ModifyDate')
        if modify_date:
            try:
                return datetime.strptime(modify_date, '%Y:%m:%d %H:%M:%S')
            except ValueError:
                pass

        # Final fallback to current date
        return datetime.now()
