"""v.2.2

Revision ID: 84f25471e582
Revises: 1e8bc65318e7
Create Date: 2024-12-12 01:56:40.626798

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "84f25471e582"
down_revision: Union[str, None] = "1e8bc65318e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT SELECT ON TABLE shops TO shop;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE SELECT ON TABLE shops FROM shop;
    """
    )
