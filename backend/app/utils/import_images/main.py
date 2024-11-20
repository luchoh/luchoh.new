import click
from pathlib import Path
from typing import Optional
from .image_processor import ImageProcessor
from .file_handler import FileHandler

@click.command()
@click.argument('source_dir', type=click.Path(exists=True))
@click.option('--recursive/--no-recursive', default=True, help='Search recursively')
@click.option('--dry-run/--no-dry-run', default=False, help='Dry run mode')
def main(source_dir: str, recursive: bool = True, dry_run: bool = False):
    """Import images from the specified directory."""
    source_path = Path(source_dir)
    file_handler = FileHandler(dry_run=dry_run)
    processor = ImageProcessor(file_handler)
    
    try:
        processor.process_directory(source_path, recursive=recursive)
    except Exception as e:
        click.echo(f"Error processing directory: {e}", err=True)
        raise

if __name__ == '__main__':
    main()