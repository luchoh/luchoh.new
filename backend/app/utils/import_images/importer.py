
import os
import sys
import click
import logging
from ...core.config import settings
from ...db.session import SessionLocal
from .processor import process_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.command()
def main():
    """Import images from Photos directory."""