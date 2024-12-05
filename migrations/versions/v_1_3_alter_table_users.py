"""v.1.3

Revision ID: aa1f2f775332
Revises: 1e9f71324674
Create Date: 2024-12-10 22:48:21.150039

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa1f2f775332"
down_revision: Union[str, None] = "1e9f71324674"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE users ADD birthdate DATE, ADD email VARCHAR(255)
    """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE users DROP COLUMN birthdate, DROP COLUMN email;
    """
    )
