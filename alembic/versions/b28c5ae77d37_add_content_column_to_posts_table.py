"""add content column to posts table

Revision ID: b28c5ae77d37
Revises: 9f938b16a273
Create Date: 2025-01-21 19:14:51.768556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b28c5ae77d37'
down_revision: Union[str, None] = '9f938b16a273'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
