"""v.3.4

Revision ID: 3d151f23ea62
Revises: a87a566aedc2
Create Date: 2024-12-12 21:44:18.802898

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d151f23ea62"
down_revision: Union[str, None] = "a87a566aedc2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE PCI_Express(
            PCI_Express_ver VARCHAR(255),
            motherboard_id UUID,
            videocard_id UUID,
            PRIMARY KEY (motherboard_id, videocard_id),
            FOREIGN KEY (motherboard_id) REFERENCES motherboard (motherboard_id),
            FOREIGN KEY (videocard_id) REFERENCES videocard (videocard_id)
        );
               
        CREATE OR REPLACE FUNCTION add_PCI_Express_on_motherboard_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO PCI_Express (motherboard_id, videocard_id, PCI_Express_ver)
            SELECT NEW.motherboard_id, videocard.videocard_id, NEW.PCI_Express_ver
            FROM videocard
            WHERE videocard.PCI_Express_ver = NEW.PCI_Express_ver;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_PCI_Express_on_motherboard_insert
        AFTER INSERT ON motherboard
        FOR EACH ROW
        EXECUTE FUNCTION add_PCI_Express_on_motherboard_insert();
        
        CREATE OR REPLACE FUNCTION add_PCI_Express_on_videocard_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO PCI_Express (motherboard_id, videocard_id, PCI_Express_ver)
            SELECT motherboard.motherboard_id, NEW.videocard_id, NEW.PCI_Express_ver
            FROM motherboard
            WHERE motherboard.PCI_Express_ver = NEW.PCI_Express_ver;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_PCI_Express_on_videocard_insert
        AFTER INSERT ON videocard
        FOR EACH ROW
        EXECUTE FUNCTION add_PCI_Express_on_videocard_insert();
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS trg_add_PCI_Express_on_videocard_insert ON videocard;
        DROP FUNCTION IF EXISTS add_PCI_Express_on_videocard_insert();
        DROP TRIGGER IF EXISTS trg_add_PCI_Express_on_motherboard_insert ON motherboard;
        DROP FUNCTION IF EXISTS add_PCI_Express_on_motherboard_insert();
        DROP TABLE IF EXISTS PCI_Express;
    """
    )
