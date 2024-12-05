"""v.5.0

Revision ID: 72fe2089998f
Revises: bb3a0dbbac8c
Create Date: 2024-12-13 23:06:06.328479

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "72fe2089998f"
down_revision: Union[str, None] = "bb3a0dbbac8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT SELECT ON TABLE shops TO regular_user;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE SELECT ON shops FROM regular_user;
    """
    )
