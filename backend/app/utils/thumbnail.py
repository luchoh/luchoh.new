import os
from PIL import Image
import face_recognition
import numpy as np


def create_smart_thumbnail(image_path, size=(200, 200)):
    # Open the image
    img = Image.open(image_path)

    # Detect faces in the image
    face_locations = face_recognition.face_locations(np.array(img))

    if face_locations:
        # If faces are found, use the first face as the center
        top, right, bottom, left = face_locations[0]
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
    else:
        # If no faces, use the center of the image
        center_x = img.width // 2
        center_y = img.height // 2

    # Calculate dimensions
    aspect_ratio = size[0] / size[1]
    if img.width / img.height > aspect_ratio:
        # Image is wider
        new_width = int(img.height * aspect_ratio)
        offset = (img.width - new_width) // 2
        crop = (offset, 0, offset + new_width, img.height)
    else:
        # Image is taller
        new_height = int(img.width / aspect_ratio)
        offset = (img.height - new_height) // 2
        crop = (0, offset, img.width, offset + new_height)

    # Crop and resize
    thumb = img.crop(crop).resize(size, Image.LANCZOS)

    # Generate thumbnail filename
    base_name = os.path.basename(image_path)
    thumb_name = f"thumb_{base_name}"
    thumb_path = os.path.join(os.path.dirname(image_path), thumb_name)

    # Save thumbnail
    thumb.save(thumb_path, "JPEG")

    return thumb_path
