"""v.5.1

Revision ID: 80a8ec6c34c1
Revises: 72fe2089998f
Create Date: 2024-12-13 23:12:04.459214

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "80a8ec6c34c1"
down_revision: Union[str, None] = "72fe2089998f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT UPDATE ON TABLE shops TO regular_user;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE UPDATE ON shops FROM regular_user;
    """
    )
