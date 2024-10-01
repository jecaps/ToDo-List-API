"""Add due_date and priority to todos

Revision ID: 1613c3341f78
Revises: 
Create Date: 2024-09-30 16:04:14.572753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1613c3341f78'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('todos', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('todos', sa.Column('priority', sa.Enum('low', 'medium', 'high', name='priority'), nullable=False, server_default='medium'))
    pass


def downgrade() -> None:
    op.drop_column('todos', 'priority')
    op.drop_column('todos', 'due_date')
    pass
