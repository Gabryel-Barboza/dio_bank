"""create user table

Revision ID: 522538604e15
Revises:
Create Date: 2025-05-07 16:48:47.040953

"""

from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '522538604e15'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid4),
        sa.Column('fullname', sa.String(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('cpf', sa.String(11), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('cpf'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user')
