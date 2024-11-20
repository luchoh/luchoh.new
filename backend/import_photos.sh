#!/bin/bash

# Ensure we're in the backend directory
cd "$(dirname "$0")"

# Set the PYTHONPATH to include the current directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run the Python script
python app/utils/import_images.py "$1"