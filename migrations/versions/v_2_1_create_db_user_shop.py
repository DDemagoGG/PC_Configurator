"""v.2.1

Revision ID: 1e8bc65318e7
Revises: e4e29ddc3f68
Create Date: 2024-12-12 01:55:37.753967

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1e8bc65318e7"
down_revision: Union[str, None] = "e4e29ddc3f68"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE USER shop WITH PASSWORD 'pswd';
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP USER IF EXISTS shop;
    """
    )
