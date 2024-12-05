"""v.4.0

Revision ID: a2bb1c764916
Revises: 3d151f23ea62
Create Date: 2024-12-12 22:02:37.637327

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2bb1c764916"
down_revision: Union[str, None] = "3d151f23ea62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE orders(
            order_id INT,
            user_id INT,
            product_id UUID,
            shop_id INT,
            status VARCHAR(255),
            product_type VARCHAR(255),
            PRIMARY KEY (order_id, product_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (shop_id) REFERENCES shops (shop_id)
        );

        CREATE SEQUENCE motherboard_order_id_seq;
        CREATE SEQUENCE ram_order_id_seq;
        CREATE SEQUENCE processor_order_id_seq;
        CREATE SEQUENCE videocard_order_id_seq;
        CREATE SEQUENCE computer_case_order_id_seq;
        CREATE SEQUENCE cooler_order_id_seq;
        CREATE SEQUENCE ssd_order_id_seq;
        CREATE SEQUENCE hdd_order_id_seq;
        CREATE SEQUENCE power_block_order_id_seq;

        GRANT usage ON SEQUENCE motherboard_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE ram_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE processor_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE videocard_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE computer_case_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE cooler_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE ssd_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE hdd_order_id_seq TO regular_user;
        GRANT usage ON SEQUENCE power_block_order_id_seq TO regular_user;

        CREATE FUNCTION set_order_id() 
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.product_type = 'motherboard' THEN
                NEW.order_id := nextval('motherboard_order_id_seq');
            ELSIF NEW.product_type = 'RAM' THEN
                NEW.order_id := nextval('ram_order_id_seq');
            ELSIF NEW.product_type = 'processor' THEN
                NEW.order_id := nextval('processor_order_id_seq');
            ELSIF NEW.product_type = 'HDD' THEN
                NEW.order_id := nextval('hdd_order_id_seq');
            ELSIF NEW.product_type = 'SSD' THEN
                NEW.order_id := nextval('ssd_order_id_seq');
            ELSIF NEW.product_type = 'computer_case' THEN
                NEW.order_id := nextval('computer_case_order_id_seq');
            ELSIF NEW.product_type = 'videocard' THEN
                NEW.order_id := nextval('videocard_order_id_seq');
            ELSIF NEW.product_type = 'cooler' THEN
                NEW.order_id := nextval('cooler_order_id_seq');
            ELSIF NEW.product_type = 'power_block' THEN
                NEW.order_id := nextval('power_block_order_id_seq');
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER order_id_trigger
        BEFORE INSERT ON orders
        FOR EACH ROW
        EXECUTE FUNCTION set_order_id();
    """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TRIGGER IF EXISTS set_order_id ON orders;
        DROP FUNCTION IF EXISTS set_order_id() CASCADE;

        REVOKE USAGE ON SEQUENCE motherboard_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE ram_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE processor_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE videocard_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE computer_case_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE cooler_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE ssd_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE hdd_order_id_seq FROM regular_user;
        REVOKE USAGE ON SEQUENCE power_block_order_id_seq FROM regular_user;

        DROP SEQUENCE motherboard_order_id_seq;
        DROP SEQUENCE ram_order_id_seq;
        DROP SEQUENCE processor_order_id_seq;
        DROP SEQUENCE videocard_order_id_seq;
        DROP SEQUENCE computer_case_order_id_seq;
        DROP SEQUENCE cooler_order_id_seq;
        DROP SEQUENCE ssd_order_id_seq;
        DROP SEQUENCE hdd_order_id_seq;
        DROP SEQUENCE power_block_order_id_seq;

        DROP TABLE IF EXISTS orders CASCADE;
    """
    )
