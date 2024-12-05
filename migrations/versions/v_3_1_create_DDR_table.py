"""v.3.1

Revision ID: 47ef9a5bf19d
Revises: 86ca49269234
Create Date: 2024-12-12 17:08:20.277677

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "47ef9a5bf19d"
down_revision: Union[str, None] = "86ca49269234"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE DDR(
            DDR_type VARCHAR(255),
            motherboard_id UUID,
            RAM_id UUID,
            PRIMARY KEY (motherboard_id, ram_id),
            FOREIGN KEY (motherboard_id) REFERENCES motherboard (motherboard_id),
            FOREIGN KEY (RAM_id) REFERENCES RAM (RAM_id)
        );
               
        CREATE OR REPLACE FUNCTION add_DDR_on_motherboard_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO DDR (motherboard_id, ram_id, DDR_type)
            SELECT NEW.motherboard_id, ram.ram_id, NEW.DDR_type
            FROM ram
            WHERE ram.DDR_type = NEW.DDR_type;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_DDR_on_motherboard_insert
        AFTER INSERT ON motherboard
        FOR EACH ROW
        EXECUTE FUNCTION add_DDR_on_motherboard_insert();
        
        CREATE OR REPLACE FUNCTION add_DDR_on_RAM_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO DDR (motherboard_id, RAM_id, DDR_type)
            SELECT motherboard.motherboard_id, NEW.RAM_id, NEW.DDR_type
            FROM motherboard
            WHERE motherboard.DDR_type = NEW.DDR_type;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_DDR_on_RAM_insert
        AFTER INSERT ON RAM
        FOR EACH ROW
        EXECUTE FUNCTION add_DDR_on_RAM_insert();
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS trg_add_DDR_on_RAM_insert ON RAM;
        DROP FUNCTION IF EXISTS add_DDR_on_RAM_insert();
        DROP TRIGGER IF EXISTS trg_add_DDR_on_motherboard_insert ON motherboard;
        DROP FUNCTION IF EXISTS add_DDR_on_motherboard_insert();
        DROP TABLE IF EXISTS DDR;
    """
    )
