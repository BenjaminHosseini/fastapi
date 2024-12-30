"""add content to posts table

Revision ID: 06b72df3fbfd
Revises: 2c9154c3f7cc
Create Date: 2024-12-30 00:13:59.412553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06b72df3fbfd'
down_revision: Union[str, None] = '2c9154c3f7cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
