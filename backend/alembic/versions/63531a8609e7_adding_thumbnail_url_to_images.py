"""Adding thumbnail_url to images

Revision ID: 63531a8609e7
Revises: c90baf1fe0c1
Create Date: 2024-07-19 12:30:38.573728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63531a8609e7'
down_revision: Union[str, None] = 'c90baf1fe0c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('thumbnail_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'thumbnail_url')
    # ### end Alembic commands ###
