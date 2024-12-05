"""v.1.0

Revision ID: a471cf112e41
Revises: 
Create Date: 2024-12-10 03:41:45.455300

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a471cf112e41"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE users(
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255),
            role VARCHAR(255)
        );
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS users;
    """
    )
