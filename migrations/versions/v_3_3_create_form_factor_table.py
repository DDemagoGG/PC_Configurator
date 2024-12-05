"""v.3.3

Revision ID: a87a566aedc2
Revises: ca0585a1f8d5
Create Date: 2024-12-12 21:41:58.810881

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a87a566aedc2"
down_revision: Union[str, None] = "ca0585a1f8d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE form_factor(
            form_factor_type VARCHAR(255),
            motherboard_id UUID,
            computer_case_id UUID,
            PRIMARY KEY (motherboard_id, computer_case_id),
            FOREIGN KEY (motherboard_id) REFERENCES motherboard (motherboard_id),
            FOREIGN KEY (computer_case_id) REFERENCES computer_case (computer_case_id)
        );
               
        CREATE OR REPLACE FUNCTION add_form_factor_on_motherboard_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO form_factor (motherboard_id, computer_case_id, form_factor_type)
            SELECT NEW.motherboard_id, computer_case.computer_case_id, NEW.form_factor_type
            FROM computer_case
            WHERE computer_case.form_factor_type = NEW.form_factor_type;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_form_factor_on_motherboard_insert
        AFTER INSERT ON motherboard
        FOR EACH ROW
        EXECUTE FUNCTION add_form_factor_on_motherboard_insert();
        
        CREATE OR REPLACE FUNCTION add_form_factor_on_computer_case_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO form_factor (motherboard_id, computer_case_id, form_factor_type)
            SELECT motherboard.motherboard_id, NEW.computer_case_id, NEW.form_factor_type
            FROM motherboard
            WHERE motherboard.form_factor_type = NEW.form_factor_type;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_add_form_factor_on_computer_case_insert
        AFTER INSERT ON computer_case
        FOR EACH ROW
        EXECUTE FUNCTION add_form_factor_on_computer_case_insert();
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS trg_add_form_factor_on_computer_case_insert ON computer_case;
        DROP FUNCTION IF EXISTS add_form_factor_on_computer_case_insert();
        DROP TRIGGER IF EXISTS trg_add_form_factor_on_motherboard_insert ON motherboard;
        DROP FUNCTION IF EXISTS add_form_factor_on_motherboard_insert();
        DROP TABLE IF EXISTS form_factor;
    """
    )
