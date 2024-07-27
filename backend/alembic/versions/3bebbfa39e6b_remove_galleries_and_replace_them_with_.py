"""Remove Galleries and replace them with Tags

Revision ID: 3bebbfa39e6b
Revises: a26c0cac4190
Create Date: 2024-07-27 23:36:40.368576

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "3bebbfa39e6b"
down_revision: Union[str, None] = "a26c0cac4190"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop foreign key constraints first
    op.drop_constraint("gallery_image_ibfk_1", "gallery_image", type_="foreignkey")
    op.drop_constraint("gallery_image_ibfk_2", "gallery_image", type_="foreignkey")

    # Drop the gallery_image table
    op.drop_table("gallery_image")

    # Drop indexes if they exist
    op.drop_index("ix_galleries_id", table_name="galleries", if_exists=True)
    op.drop_index("ix_galleries_title", table_name="galleries", if_exists=True)

    # Drop the galleries table
    op.drop_table("galleries")

    # Add new columns to tags table
    op.add_column(
        "tags", sa.Column("description", sa.String(length=500), nullable=True)
    )
    op.add_column("tags", sa.Column("order", sa.Integer(), nullable=True))


def downgrade() -> None:
    # Remove new columns from tags table
    op.drop_column("tags", "order")
    op.drop_column("tags", "description")

    # Recreate galleries table
    op.create_table(
        "galleries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Recreate indexes
    op.create_index("ix_galleries_title", "galleries", ["title"], unique=False)
    op.create_index("ix_galleries_id", "galleries", ["id"], unique=False)

    # Recreate gallery_image table
    op.create_table(
        "gallery_image",
        sa.Column("gallery_id", sa.Integer(), nullable=True),
        sa.Column("image_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["gallery_id"], ["galleries.id"], name="gallery_image_ibfk_1"
        ),
        sa.ForeignKeyConstraint(
            ["image_id"], ["images.id"], name="gallery_image_ibfk_2"
        ),
    )
