# Project: luchoh.com refactoring
# File: backend/commands.py
from app.schemas.user import UserCreate
from app.crud.user import user
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    if not superusers:
        print("No superusers found.")
        return
    print("\nSuperusers:")
    for su in superusers:
        print(f"Username: {su.username}, Email: {su.email}")

def change_superuser_password(username: str, new_password: str):
    db = SessionLocal()
    db_user = user.get_by_username(db, username)
    if not db_user:
        print(f"User {username} not found.")
        db.close()
        return
    if not db_user.is_superuser:
        print(f"User {username} is not a superuser.")
        db.close()
        return
    
    db_user.hashed_password = get_password_hash(new_password)
    db.add(db_user)
    db.commit()
    db.close()
    print(f"Password changed successfully for superuser {username}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Available commands:")
        print("  create_superuser <username> <email> <password>")
        print("  list_superusers")
        print("  change_superuser_password <username> <new_password>")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "create_superuser":
        if len(sys.argv) != 5:
            print("Usage: python commands.py create_superuser <username> <email> <password>")
            sys.exit(1)
        username, email, password = sys.argv[2:]
        create_superuser(username, email, password)
    elif command == "list_superusers":
        list_superusers()
    elif command == "change_superuser_password":
        if len(sys.argv) != 4:
            print("Usage: python commands.py change_superuser_password <username> <new_password>")
            sys.exit(1)
        username, new_password = sys.argv[2:]
        change_superuser_password(username, new_password)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)