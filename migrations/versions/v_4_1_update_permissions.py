"""v.4.1

Revision ID: e3434a9726d2
Revises: a2bb1c764916
Create Date: 2024-12-12 22:31:47.696967

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e3434a9726d2"
down_revision: Union[str, None] = "a2bb1c764916"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT SELECT ON TABLE orders TO shop;
        GRANT INSERT ON TABLE orders TO regular_user;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE SELECT ON orders FROM shop;
        REVOKE INSERT ON orders FROM regular_user;
    """
    )
