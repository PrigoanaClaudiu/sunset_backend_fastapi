"""create reviews table

Revision ID: c4820a0d2a4b
Revises: 
Create Date: 2024-08-03 23:48:06.288142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4820a0d2a4b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("reviews", sa.Column('id', sa.Integer(), nullable=False, primary_key=True))


def downgrade() -> None:
    op.drop_table('posts')
    pass
