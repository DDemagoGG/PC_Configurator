"""v.2.0

Revision ID: e4e29ddc3f68
Revises: aa1f2f775332
Create Date: 2024-12-12 01:52:14.928909

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e4e29ddc3f68"
down_revision: Union[str, None] = "aa1f2f775332"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE shops(
            shop_id SERIAL PRIMARY KEY,
            shopname VARCHAR(255),
            password VARCHAR(255),
            address VARCHAR(255)
        );
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS shops;
    """
    )
