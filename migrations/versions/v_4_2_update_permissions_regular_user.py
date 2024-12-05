"""v.4.2

Revision ID: 9520c2516619
Revises: e3434a9726d2
Create Date: 2024-12-12 23:05:47.978529

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9520c2516619"
down_revision: Union[str, None] = "e3434a9726d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT SELECT ON TABLE orders TO regular_user;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE SELECT ON orders FROM regular_user;
    """
    )
