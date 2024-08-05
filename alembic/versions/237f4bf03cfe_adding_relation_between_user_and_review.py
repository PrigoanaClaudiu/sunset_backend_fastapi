"""adding relation between user and review

Revision ID: 237f4bf03cfe
Revises: 0a75cdc5b163
Create Date: 2024-08-04 00:59:34.103306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '237f4bf03cfe'
down_revision: Union[str, None] = '0a75cdc5b163'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('fk_reviews_users', 'reviews', 'users', ['user_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('fk_reviews_users', 'reviews', type_='foreignkey')