# Project: luchoh.com refactoring
# File: backend/commands.py
import sys
import os
import getpass

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.crud.user import user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.models.user import User  # Import the User model

def create_superuser(username: str, email: str, password: str):
    db = SessionLocal()
    user_in = UserCreate(
        username=username, email=email, password=password, is_superuser=True
    )
    user.create(db, user_in)
    db.close()
    print(f"Superuser {username} created successfully.")

def list_superusers():
    db = SessionLocal()
    superusers = db.query(User).filter(User.is_superuser == True).all()
    db.close()
    if superusers:
        print("Superusers:")
        for su in superusers:
            print(f"ID: {su.id}, Username: {su.username}, Email: {su.email}")
    else:
        print("No superusers found.")

def change_superuser_password(username: str):
    db = SessionLocal()
    db_user = user.get_by_username(db, username)
    if db_user and db_user.is_superuser:
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        if new_password == confirm_password:
            hashed_password = get_password_hash(new_password)
            db_user.hashed_password = hashed_password
            db.commit()
            print(f"Password for superuser {username} updated successfully.")
        else:
            print("Passwords do not match. Password not updated.")
    else:
        print(f"Superuser {username} not found.")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python commands.py <command> [args...]")
        print("Commands:")
        print("  create_superuser <username> <email> <password>")
        print("  list_superusers")
        print("  change_superuser_password <username>")
    else:
        command = sys.argv[1]
        if command == "create_superuser" and len(sys.argv) == 5:
            _, _, username, email, password = sys.argv
            create_superuser(username, email, password)
        elif command == "list_superusers":
            list_superusers()
        elif command == "change_superuser_password" and len(sys.argv) == 3:
            _, _, username = sys.argv
            change_superuser_password(username)
        else:
            print(f"Unknown command or incorrect number of arguments: {command}")
