
import os
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.image import Image
from app.core.config import settings
from app.db.session import get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_duplicate_images(db):
    """Get all duplicate images based on file_hash."""
    # First, get all file_hashes that appear more than once
    duplicate_hashes = (
        db.query(Image.file_hash)
        .filter(Image.file_hash.isnot(None))
        .group_by(Image.file_hash)
        .having(db.func.count(Image.id) > 1)
        .all()
    )
    
    duplicate_images = []
    for hash_tuple in duplicate_hashes:
        file_hash = hash_tuple[0]
        # Get all images with this hash, ordered by id (keep the oldest)
        images = (
            db.query(Image)
            .filter(Image.file_hash == file_hash)
            .order_by(Image.id)
            .all()
        )
        # Add all but the first (oldest) image to the duplicates list
        duplicate_images.extend(images[1:])
    
    return duplicate_images

def delete_image_file(file_path):
    """Delete image file and its thumbnail if they exist."""
    try:
        # Delete main image
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
        
        # Check for and delete thumbnail
        thumbnail_path = os.path.join(
            os.path.dirname(file_path),
            'thumbnail_' + os.path.basename(file_path)
        )
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
            logger.info(f"Deleted thumbnail: {thumbnail_path}")
            
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")

@click.group()
def cli():
    """Image database cleanup utility."""
    pass

@cli.command()
@click.option('--dry-run', is_flag=True, help='Show what would be deleted without actually deleting')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def clear_all(dry_run, force):
    """Clear all images from the database."""
    db = next(get_db())
    
    try:
        # Get count of all images
        total_images = db.query(Image).count()
        logger.info(f"Found {total_images} images in database")
        
        if total_images == 0:
            logger.info("No images to delete")
            return
        
        if not dry_run and not force:
            click.confirm(f'Are you sure you want to delete all {total_images} images?', abort=True)
        
        images = db.query(Image).all()
        
        for image in images:
            if dry_run:
                logger.info(f"Would delete image: {image.title} (ID: {image.id})")
            else:
                # Delete the actual file
                if image.file_path:
                    delete_image_file(image.file_path)
                
                # Delete from database
                db.delete(image)
                logger.info(f"Deleted image: {image.title} (ID: {image.id})")
        
        if not dry_run:
            db.commit()
            logger.info("All images have been deleted")
        else:
            logger.info("Dry run completed - no changes made")
            
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        db.rollback()
    finally:
        db.close()

@cli.command()
@click.option('--dry-run', is_flag=True, help='Show what would be deleted without actually deleting')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def clear_duplicates(dry_run, force):
    """Clear duplicate images from the database."""