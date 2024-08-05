"""add more columns to reviews

Revision ID: 2959385b258d
Revises: c4820a0d2a4b
Create Date: 2024-08-04 00:43:50.308863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2959385b258d'
down_revision: Union[str, None] = 'c4820a0d2a4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('reviews', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('content', sa.Text(), nullable=False))
    op.add_column('reviews', sa.Column('rating', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('created_at',postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    # op.create_foreign_key(None, 'reviews', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'user_id')
    op.drop_column('reviews', 'content')
    op.drop_column('reviews', 'rating')
    op.drop_column('reviews', 'created_at')
