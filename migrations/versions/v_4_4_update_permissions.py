"""v.4.4

Revision ID: bb3a0dbbac8c
Revises: cc1bd5f94688
Create Date: 2024-12-13 05:45:21.395421

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bb3a0dbbac8c"
down_revision: Union[str, None] = "cc1bd5f94688"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT SELECT ON TABLE RAM TO regular_user;
        GRANT SELECT ON TABLE processor TO regular_user;
        GRANT SELECT ON TABLE cooler TO regular_user;
        GRANT SELECT ON TABLE computer_case TO regular_user;
        GRANT SELECT ON TABLE videocard TO regular_user;
        GRANT SELECT ON TABLE power_block TO regular_user;
        GRANT SELECT ON TABLE HDD TO regular_user;
        GRANT SELECT ON TABLE SSD TO regular_user;
        GRANT SELECT ON TABLE motherboard TO regular_user;
        
        GRANT SELECT ON TABLE RAM TO shop;
        GRANT SELECT ON TABLE processor TO shop;
        GRANT SELECT ON TABLE cooler TO shop;
        GRANT SELECT ON TABLE computer_case TO shop;
        GRANT SELECT ON TABLE videocard TO shop;
        GRANT SELECT ON TABLE power_block TO shop;
        GRANT SELECT ON TABLE HDD TO shop;
        GRANT SELECT ON TABLE SSD TO shop;
        GRANT SELECT ON TABLE motherboard TO shop;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE SELECT ON RAM FROM regular_user;
        REVOKE SELECT ON processor FROM regular_user;
        REVOKE SELECT ON cooler FROM regular_user;
        REVOKE SELECT ON computer_case FROM regular_user;
        REVOKE SELECT ON videocard FROM regular_user;
        REVOKE SELECT ON power_block FROM regular_user;
        REVOKE SELECT ON HDD FROM regular_user;
        REVOKE SELECT ON SSD FROM regular_user;
        REVOKE SELECT ON motherboard FROM regular_user;
        
        REVOKE SELECT ON RAM FROM shop;
        REVOKE SELECT ON processor FROM shop;
        REVOKE SELECT ON cooler FROM shop;
        REVOKE SELECT ON computer_case FROM shop;
        REVOKE SELECT ON videocard FROM shop;
        REVOKE SELECT ON power_block FROM shop;
        REVOKE SELECT ON HDD FROM shop;
        REVOKE SELECT ON SSD FROM shop;
        REVOKE SELECT ON motherboard FROM shop;
    """
    )
