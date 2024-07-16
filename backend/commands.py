import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.crud.user import user
from app.schemas.user import UserCreate


def create_superuser(username: str, email: str, password: str):
    db = SessionLocal()
    user_in = UserCreate(
        username=username, email=email, password=password, is_superuser=True
    )
    user.create(db, user_in)
    db.close()
    print(f"Superuser {username} created successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 5:  # Changed from 4 to 5
        print(
            "Usage: python commands.py create_superuser <username> <email> <password>"
        )
    else:
        command, username, email, password = sys.argv[1:]  # Changed this line
        if command == "create_superuser":
            create_superuser(username, email, password)
        else:
            print(f"Unknown command: {command}")
