"""v.5.3


Revision ID: d55bfa6e6aa1
Revises: 4a14873fd6bb
Create Date: 2024-12-18 05:26:38.267898

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d55bfa6e6aa1"
down_revision: Union[str, None] = "4a14873fd6bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT UPDATE ON TABLE orders TO shop;
"""
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE UPDATE ON orders FROM shop;
"""
    )
