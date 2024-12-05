"""v.1.2

Revision ID: 1e9f71324674
Revises: e671142c5efe
Create Date: 2024-12-10 19:11:20.177250

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1e9f71324674"
down_revision: Union[str, None] = "e671142c5efe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT UPDATE, INSERT ON users TO regular_user;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO regular_user;
        GRANT usage ON SEQUENCE users_user_id_seq TO regular_user;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE UPDATE, INSERT ON users FROM regular_user;
        REVOKE SELECT ON ALL TABLES IN SCHEMA public FROM regular_user;
        REVOKE USAGE ON SEQUENCE users_user_id_seq FROM regular_user;
    """
    )
