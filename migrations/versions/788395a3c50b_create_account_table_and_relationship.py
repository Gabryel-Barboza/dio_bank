"""create account table and relationship

Revision ID: 788395a3c50b
Revises: 522538604e15
Create Date: 2025-05-07 16:51:01.679268

"""

from decimal import Decimal
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

from src.models import AccountType

# revision identifiers, used by Alembic.
revision: str = '788395a3c50b'
down_revision: Union[str, None] = '522538604e15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'account',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid4),
        sa.Column('account_no', sa.Integer(), nullable=False),
        sa.Column(
            'id_user',
            sa.UUID(),
            sa.ForeignKey('user.id', ondelete='CASCADE'),
            nullable=True,
        ),
        sa.Column(
            'account_type',
            sa.Enum(AccountType),
            nullable=False,
            default=AccountType.corrente,
        ),
        sa.Column(
            'balance',
            sa.Numeric(precision=10, scale=2),
            nullable=False,
            default=Decimal(),
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('account')
