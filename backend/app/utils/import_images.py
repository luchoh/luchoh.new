import os
from datetime import datetime
import exifread
from tqdm import tqdm
import requests
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings

def get_image_date(file_path: str) -> datetime:
    """Get image date from EXIF data or file modification date."""
    # For PNG files, directly use file modification time
    if file_path.lower().endswith('.png'):
        return datetime.fromtimestamp(os.path.getmtime(file_path))

    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
            if 'EXIF DateTimeOriginal' in tags:
                date_str = str(tags['EXIF DateTimeOriginal'])
                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Could not read EXIF data, using file date for {file_path}")
    
    # Fallback to file modification time
    return datetime.fromtimestamp(os.path.getmtime(file_path))

def get_next_take_number(db: Session) -> int:
    """Get the next available take number by checking existing titles."""
    from app.models.image import Image
    max_take = 0
    
    images = db.query(Image).all()
    for img in images:
        if img.title.startswith('Take '):
            try:
                take_num = int(img.title.split(' ')[1])
                max_take = max(max_take, take_num)
            except (IndexError, ValueError):
                continue
    
    return max_take + 1

def import_folder(folder_path: str, take_number: int, headers: dict) -> bool:
    """Import all images from a folder."""
    image_files = [f for f in os.listdir(folder_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if not image_files:
        print(f"No images found in {folder_path}")
        return False

    # Get folder name for title and tag
    folder_name = os.path.basename(folder_path)

    # Filter out zero-size (not downloaded) files
    valid_files = []
    for filename in image_files:
        file_path = os.path.join(folder_path, filename)
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"Skipping {filename} - file not downloaded (0 bytes)")
            continue
        valid_files.append(filename)

    if not valid_files:
        print(f"No valid images found in {folder_path}")
        return False
    
    with tqdm(total=len(valid_files), desc=f"Importing {folder_name}") as pbar:
        for idx, filename in enumerate(valid_files, 1):
            file_path = os.path.join(folder_path, filename)
            image_date = get_image_date(file_path)
            title = f"{folder_name} Take {idx}, {image_date.year}"
            
            # Prepare multipart form data
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'image/jpeg')}
                data = {
                    'title': title,
                    'description': f'Imported from {folder_name}',
                    'sticky': 'false',
                    'tags': folder_name  # Add the folder name as a tag
                }
                
                try:
                    api_url = f"http://localhost:8008{settings.API_V1_STR}/images/"
                    response = requests.post(
                        api_url,
                        files=files,
                        data=data,
                        headers=headers
                    )
                    response.raise_for_status()
                except Exception as e:
                    print(f"Error uploading {filename}: {str(e)}")
            
            pbar.update(1)
    
    return True

def main() -> None:
    """Main function called by the import script."""
    if len(os.sys.argv) != 2:
        print("Usage: import_photos.sh <dropbox_folder_path>")
        return

    dropbox_path = os.sys.argv[1]
    if not os.path.exists(dropbox_path):
        print(f"Path does not exist: {dropbox_path}")
        return

    # Get credentials from user
    from getpass import getpass
    username = input("Username: ")
    password = getpass("Password: ")

    # Authenticate
    auth_response = requests.post(
        "http://localhost:8008/api/v1/auth/token",
        data={"username": username, "password": password}
    )
    if not auth_response.ok:
        print("Authentication failed")
        return
    
    token = auth_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    db = SessionLocal()
    try:
        folders = [f for f in os.listdir(dropbox_path) 
                  if os.path.isdir(os.path.join(dropbox_path, f))]
        folders.sort()

        take_number = get_next_take_number(db)
        
        for folder in folders:
            folder_path = os.path.join(dropbox_path, folder)
            if input(f"Import {folder}? (y/n): ").lower().startswith('y'):
                # Create tag only if user wants to process this folder
                try:
                    tag_response = requests.post(
                        f"http://localhost:8008{settings.API_V1_STR}/tags/",
                        headers=headers,
                        json={"name": folder, "description": f"Images from {folder}"}
                    )
                    if not tag_response.ok and tag_response.status_code != 400:  # 400 means tag exists
                        print(f"Error creating tag: {tag_response.text}")
                        continue
                except Exception as e:
                    print(f"Error creating tag: {str(e)}")
                    continue

                if import_folder(folder_path, take_number, headers):
                    take_number += 1
        
        print("Import complete!")
    finally:
        db.close()

if __name__ == '__main__':
    main()