"""create transaction table

Revision ID: 0505a18264b6
Revises: 788395a3c50b
Create Date: 2025-05-07 16:53:44.733743

"""

from datetime import datetime, timezone
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from src.models import TransactionType

# revision identifiers, used by Alembic.
revision: str = '0505a18264b6'
down_revision: Union[str, None] = '788395a3c50b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'transaction',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('transaction_no', sa.Integer(), nullable=False),
        sa.Column(
            'id_account',
            sa.UUID(),
            sa.ForeignKey('account.id', ondelete='CASCADE'),
            nullable=True,
        ),
        sa.Column('transaction_type', sa.Enum(TransactionType), nullable=False),
        sa.Column(
            'transaction_value', sa.Numeric(precision=10, scale=2), nullable=False
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            nullable=True,
            default=datetime.now(timezone.utc),
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('transaction')
