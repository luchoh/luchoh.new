"""Generate all tables

Revision ID: 07f9763630a3
Revises: 
Create Date: 2024-07-17 02:21:16.775382

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "07f9763630a3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("hashed_password", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    # Create galleries table
    op.create_table(
        "galleries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_galleries_id"), "galleries", ["id"], unique=False)
    op.create_index(op.f("ix_galleries_title"), "galleries", ["title"], unique=False)

    # Create images table
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("file_path", sa.String(length=255), nullable=True),
        sa.Column("gallery_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["gallery_id"],
            ["galleries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_images_id"), "images", ["id"], unique=False)
    op.create_index(op.f("ix_images_title"), "images", ["title"], unique=False)


def downgrade() -> None:
    op.drop_table("images")
    op.drop_table("galleries")
    op.drop_table("users")
