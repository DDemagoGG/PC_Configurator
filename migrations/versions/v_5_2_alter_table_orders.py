"""v.5.2

Revision ID: 4a14873fd6bb
Revises: 80a8ec6c34c1
Create Date: 2024-12-13 23:13:28.551870

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4a14873fd6bb"
down_revision: Union[str, None] = "80a8ec6c34c1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE orders ADD COLUMN creation_time TIMESTAMP;
        ALTER TABLE orders ADD COLUMN completion_time TIMESTAMP;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE orders DROP COLUMN creation_time;
        ALTER TABLE orders DROP COLUMN completion_time;
    """
    )
