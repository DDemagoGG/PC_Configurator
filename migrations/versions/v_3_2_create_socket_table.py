"""v.3.2

Revision ID: ca0585a1f8d5
Revises: 47ef9a5bf19d
Create Date: 2024-12-12 21:36:45.845093

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ca0585a1f8d5"
down_revision: Union[str, None] = "47ef9a5bf19d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE socket(
            socket_type VARCHAR(255),
            motherboard_id UUID,
            processor_id UUID,
            PRIMARY KEY (motherboard_id, processor_id),
            FOREIGN KEY (motherboard_id) REFERENCES motherboard (motherboard_id),
            FOREIGN KEY (processor_id) REFERENCES processor (processor_id)
        );
               
        CREATE OR REPLACE FUNCTION add_socket_on_motherboard_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO socket (motherboard_id, processor_id, socket_type)
            SELECT NEW.motherboard_id, processor.processor_id, NEW.socket_type
            FROM processor
            WHERE processor.socket_type = NEW.socket_type;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_socket_on_motherboard_insert
        AFTER INSERT ON motherboard
        FOR EACH ROW
        EXECUTE FUNCTION add_socket_on_motherboard_insert();
        
        CREATE OR REPLACE FUNCTION add_socket_on_processor_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO socket (motherboard_id, processor_id, socket_type)
            SELECT motherboard.motherboard_id, NEW.processor_id, NEW.socket_type
            FROM motherboard
            WHERE motherboard.socket_type = NEW.socket_type;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_socket_on_processor_insert
        AFTER INSERT ON processor
        FOR EACH ROW
        EXECUTE FUNCTION add_socket_on_processor_insert();
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS trg_add_socket_on_processor_insert ON processor;
        DROP FUNCTION IF EXISTS add_socket_on_processor_insert();
        DROP TRIGGER IF EXISTS trg_add_socket_on_motherboard_insert ON motherboard;
        DROP FUNCTION IF EXISTS add_socket_on_motherboard_insert();
        DROP TABLE IF EXISTS socket;
    """
    )
