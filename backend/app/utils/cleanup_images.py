
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.utils.cleanup import cli

if __name__ == '__main__':
    cli()