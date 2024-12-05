"""v.1.1

Revision ID: e671142c5efe
Revises: a471cf112e41
Create Date: 2024-12-10 04:09:24.837754

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e671142c5efe"
down_revision: Union[str, None] = "a471cf112e41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE USER regular_user WITH PASSWORD 'pswd';
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP USER IF EXISTS regular_user;
    """
    )
