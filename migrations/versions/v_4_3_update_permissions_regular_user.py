"""v.4.3

Revision ID: cc1bd5f94688
Revises: 9520c2516619
Create Date: 2024-12-13 00:11:02.116097

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cc1bd5f94688"
down_revision: Union[str, None] = "9520c2516619"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        GRANT SELECT ON TABLE DDR TO regular_user;
        GRANT SELECT ON TABLE form_factor TO regular_user;  
        GRANT SELECT ON TABLE PCI_Express TO regular_user;
        GRANT SELECT ON TABLE socket TO regular_user;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        REVOKE SELECT ON DDR FROM regular_user;
        REVOKE SELECT ON form_factor FROM regular_user;  
        REVOKE SELECT ON PCI_Express FROM regular_user;
        REVOKE SELECT ON socket FROM regular_user;
    """
    )
