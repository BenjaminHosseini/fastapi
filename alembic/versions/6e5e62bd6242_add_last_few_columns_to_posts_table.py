"""add last few columns to posts table

Revision ID: 6e5e62bd6242
Revises: 8e2b11700d63
Create Date: 2024-12-30 00:40:44.977400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e5e62bd6242'
down_revision: Union[str, None] = '8e2b11700d63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
   op.add_column('posts', sa.Column('creted_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_defalult=sa.text('NOW()')),)
   pass


def downgrade() -> None:
    op.drop_column('posts' 'published')
    op.drop_column('posts', 'created_at')
    pass
