
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.cleanup import cli

if __name__ == '__main__':
    cli()