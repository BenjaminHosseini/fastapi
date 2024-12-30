"""create post table

Revision ID: 2c9154c3f7cc
Revises: 
Create Date: 2024-12-28 17:42:21.997905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c9154c3f7cc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#creating tables
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    pass

# droping  tables
def downgrade() -> None:
    op.drop_table('posts')
    pass
