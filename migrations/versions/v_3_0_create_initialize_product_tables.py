"""v.3.0

Revision ID: 86ca49269234
Revises: 84f25471e582
Create Date: 2024-12-12 04:09:17.928979

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "86ca49269234"
down_revision: Union[str, None] = "84f25471e582"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE TABLE RAM(
            RAM_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            manufacturer VARCHAR(255),
            model VARCHAR(255),
            capacity INTEGER,
            DDR_type VARCHAR(255),
            frequency INTEGER,
            price INTEGER
        );
        CREATE TABLE processor(
            processor_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            cores_num INT,
            manufacturer VARCHAR(255), 
            family VARCHAR(255),
            model VARCHAR(255),
            frequency DECIMAL,
            cash_capacity INTEGER,
            socket_type VARCHAR(255),
            price INTEGER
        );
        CREATE TABLE cooler(
            cooler_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            type VARCHAR(255),
            price INTEGER,
            model VARCHAR(255)
        );
        CREATE TABLE computer_case(
            computer_case_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            price INTEGER,
            manufacturer VARCHAR(255),
            form_factor_type VARCHAR(255),
            model VARCHAR(255),
            tower_size VARCHAR(255),
            main_color VARCHAR(255)
        );
        CREATE TABLE videocard(
            videocard_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            manufacturer VARCHAR(255),
            videomemory_capacity INTEGER,
            memory_bus_width INTEGER,
            memory_type VARCHAR(255),
            PCI_Express_ver VARCHAR(255),
            model VARCHAR(255),
            price INTEGER
        );
        CREATE TABLE power_block(
            power_block_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            manufacturer VARCHAR(255),
            price INTEGER,
            power INTEGER, 
            model VARCHAR(255)
        );
        CREATE TABLE HDD(
            HDD_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            manufacturer VARCHAR(255),
            capacity INTEGER,
            recording_technology VARCHAR(255),
            cash_capacity INTEGER,
            model VARCHAR(255),
            price INTEGER
        );
        CREATE TABLE SSD(
            SSD_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            manufacturer VARCHAR(255),
            capacity INTEGER,
            max_read_speed INTEGER,
            max_write_speed INTEGER,
            model VARCHAR(255),
            price INTEGER
        );
        CREATE TABLE motherboard(
            motherboard_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            socket_type VARCHAR(255),
            manufacturer VARCHAR(255),
            DDR_type VARCHAR(255),
            form_factor_type VARCHAR(255),
            chipset VARCHAR(255),
            memory_slot_num INTEGER,
            PCI_Express_ver VARCHAR(255),
            M2_port_num INTEGER,
            model VARCHAR(255),
            price INTEGER
        );

        INSERT INTO RAM (manufacturer, model, capacity, DDR_type, frequency, price) VALUES
        ('Kingston', 'HyperX Fury', 16, 'DDR4', 3200, 85),
        ('Corsair', 'Vengeance LPX', 8, 'DDR4', 3000, 40),
        ('G.Skill', 'Trident Z', 32, 'DDR4', 3600, 160),
        ('Crucial', 'Ballistix', 16, 'DDR4', 2666, 70),
        ('Samsung', 'M378A1G43EB1', 8, 'DDR4', 2400, 35),
        ('Kingston', 'ValueRAM', 16, 'DDR3', 1600, 50),
        ('Corsair', 'Vengeance Pro', 16, 'DDR3', 1866, 55),
        ('G.Skill', 'Ripjaws V', 8, 'DDR4', 2133, 30),
        ('Crucial', 'Ballistix Max', 32, 'DDR4', 4000, 200),
        ('Samsung', 'M391A2K43BB1', 16, 'DDR4', 2666, 90),
        ('Kingston', 'HyperX Impact', 8, 'DDR3', 1600, 45),
        ('Corsair', 'Vengeance RGB Pro', 16, 'DDR4', 3200, 95),
        ('G.Skill', 'Aegis', 8, 'DDR4', 2133, 25),
        ('Crucial', 'Ballistix Elite', 16, 'DDR4', 3600, 110),
        ('Samsung', 'M471A5244CB0', 4, 'DDR4', 2133, 20);

        INSERT INTO processor (cores_num, manufacturer, family, model, frequency, cash_capacity, socket_type, price) VALUES
        (6, 'Intel', 'Core i5', '10400F', 2.9, 12, 'LGA1200', 150),
        (8, 'AMD', 'Ryzen 7', '5800X', 3.8, 32, 'AM4', 350),
        (4, 'Intel', 'Core i3', '10100', 3.6, 6, 'LGA1200', 110),
        (16, 'AMD', 'Ryzen 9', '5950X', 3.4, 64, 'AM4', 750),
        (10, 'Intel', 'Core i9', '10900K', 3.7, 20, 'LGA1200', 500),
        (6, 'AMD', 'Ryzen 5', '3600', 3.6, 32, 'AM4', 200),
        (4, 'Intel', 'Pentium', 'G6400', 4, 4, 'LGA1200', 65),
        (6, 'AMD', 'Ryzen 5', '5600X', 3.7, 35, 'AM4', 280),
        (8, 'Intel', 'Core i7', '11700', 2.9, 16, 'LGA1200', 300),
        (12, 'AMD', 'Ryzen 7', '5900X', 3.7, 64, 'AM4', 500),
        (6, 'Intel', 'Core i5', '10500', 3.1, 12, 'LGA1200', 190),
        (8, 'AMD', 'Ryzen 7', '3700X', 3.6, 32, 'AM4', 330),
        (2, 'Intel', 'Celeron', 'G5905', 3.5, 2, 'LGA1200', 50),
        (12, 'Intel', 'Xeon', 'W-1290', 3.2, 16, 'LGA1200', 600),
        (16, 'AMD', 'Threadripper', '3990X', 2.9, 256, 'TRX40', 4000);

        INSERT INTO cooler (type, price, model) VALUES
        ('Air', 50, 'Cooler Master Hyper 212'),
        ('Water', 100, 'NZXT Kraken X53'),
        ('Air', 35, 'Arctic Freezer 34'),
        ('Water', 150, 'Corsair iCUE H150i'),
        ('Air', 25, 'DeepCool GAMMAXX 400'),
        ('Water', 120, 'Thermaltake Floe DX 240'),
        ('Air', 70, 'Noctua NH-D15'),
        ('Water', 130, 'ASUS ROG RYUO 240'),
        ('Air', 40, 'Be Quiet! Dark Rock 4'),
        ('Water', 140, 'MSI MAG CORELIQUID 360R'),
        ('Air', 30, 'Zalman CNPS10X'),
        ('Water', 110, 'EVGA CLC 240'),
        ('Air', 45, 'Scythe Mugen 5'),
        ('Water', 160, 'Alphacool Eisbaer LT240'),
        ('Air', 20, 'Thermaltake UX200');

        INSERT INTO computer_case (price, manufacturer, form_factor_type, model, tower_size, main_color) VALUES
        (70, 'Cooler Master', 'ATX', 'MasterBox Q300L', 'Mid Tower', 'Black'),
        (120, 'NZXT', 'ATX', 'H510 Elite', 'Mid Tower', 'White'),
        (50, 'Thermaltake', 'Micro-ATX', 'V150', 'Mini Tower', 'Black'),
        (90, 'Corsair', 'ATX', 'iCUE 4000X', 'Mid Tower', 'Black'),
        (40, 'DeepCool', 'ATX', 'MATREXX 30', 'Mid Tower', 'Black'),
        (60, 'Be Quiet!', 'ATX', 'Pure Base 500', 'Mid Tower', 'Gray'),
        (100, 'Phanteks', 'E-ATX', 'Eclipse P600S', 'Full Tower', 'Black'),
        (110, 'Lian Li', 'Mini-ITX', 'PC-O11D Mini', 'Mid Tower', 'White'),
        (55, 'Zalman', 'Micro-ATX', 'T7', 'Mini Tower', 'Black'),
        (80, 'SilverStone', 'ATX', 'FARA R1', 'Mid Tower', 'Black'),
        (45, 'Cougar', 'Mini-ITX', 'QBX', 'Mini Tower', 'Gray'),
        (75, 'Fractal Design', 'ATX', 'Meshify C', 'Mid Tower', 'White'),
        (85, 'InWin', 'ATX', '101', 'Mid Tower', 'Black'),
        (65, 'BitFenix', 'Micro-ATX', 'Prodigy M', 'Mini Tower', 'Black'),
        (95, 'Thermaltake', 'ATX', 'Level 20 MT', 'Mid Tower', 'Black');

        INSERT INTO videocard (manufacturer, videomemory_capacity, memory_bus_width, memory_type, PCI_Express_ver, model, price) VALUES
        ('NVIDIA', 8, 256, 'GDDR6', '4.0', 'RTX 3070', 500),
        ('AMD', 16, 256, 'GDDR6', '4.0', 'RX 6800 XT', 650),
        ('NVIDIA', 6, 192, 'GDDR6', '4.0', 'RTX 3060', 330),
        ('AMD', 8, 128, 'GDDR5', '3.0', 'RX 5500 XT', 200),
        ('NVIDIA', 10, 320, 'GDDR6X', '4.0', 'RTX 3080', 800),
        ('AMD', 4, 128, 'GDDR5', '3.0', 'RX 560', 150),
        ('NVIDIA', 24, 384, 'GDDR6X', '4.0', 'RTX 3090', 1500),
        ('AMD', 12, 192, 'GDDR6', '4.0', 'RX 6700 XT', 480),
        ('NVIDIA', 8, 256, 'GDDR6', '3.0', 'GTX 1070', 400),
        ('AMD', 6, 192, 'GDDR6', '3.0', 'RX 590', 300),
        ('NVIDIA', 4, 128, 'GDDR5', '3.0', 'GTX 1050 Ti', 180),
        ('AMD', 8, 256, 'GDDR5', '3.0', 'RX 480', 250),
        ('NVIDIA', 16, 256, 'GDDR6', '4.0', 'RTX 2080 Ti', 1200),
        ('AMD', 8, 128, 'GDDR6', '4.0', 'RX 6600', 330),
        ('NVIDIA', 12, 192, 'GDDR6X', '4.0', 'RTX 3060 Ti', 400);

        INSERT INTO power_block (manufacturer, price, power, model) VALUES
        ('Corsair', 80, 650, 'RM650x'),
        ('Cooler Master', 60, 550, 'MWE Gold 550'),
        ('Seasonic', 100, 750, 'Focus GX-750'),
        ('Thermaltake', 55, 500, 'Smart BX1'),
        ('EVGA', 90, 700, 'SuperNOVA 700 G1'),
        ('Be Quiet!', 110, 850, 'Dark Power Pro 11'),
        ('Corsair', 75, 600, 'CX600M'),
        ('Cooler Master', 50, 450, 'Elite V3'),
        ('Seasonic', 120, 1000, 'PRIME TX-1000'),
        ('Thermaltake', 40, 400, 'Litepower 400W'),
        ('EVGA', 70, 650, 'B5 650W'),
        ('Be Quiet!', 85, 700, 'Pure Power 11'),
        ('Corsair', 65, 500, 'VS500'),
        ('Cooler Master', 130, 850, 'V850 Gold V2'),
        ('Seasonic', 90, 650, 'Focus PX-650');

        INSERT INTO HDD (manufacturer, capacity, recording_technology, cash_capacity, model, price) VALUES
        ('Western Digital', 1024, 'CMR', 64, 'WD Blue', 45),
        ('Seagate', 2048, 'SMR', 128, 'Barracuda', 65),
        ('Toshiba', 1024, 'CMR', 32, 'P300', 50),
        ('Western Digital', 4096, 'CMR', 256, 'WD Red', 110),
        ('Seagate', 4096, 'CMR', 256, 'IronWolf', 180),
        ('Toshiba', 2048, 'SMR', 64, 'L200', 70),
        ('Western Digital', 8192, 'CMR', 256, 'WD Gold', 230),
        ('Seagate', 2048, 'CMR', 128, 'SkyHawk', 90),
        ('Toshiba', 512, 'SMR', 16, 'DT01ACA050', 35),
        ('Western Digital', 4096, 'CMR', 512, 'Ultrastar', 400),
        ('Seagate', 1024, 'SMR', 64, 'Barracuda Compute', 40),
        ('Toshiba', 4096, 'CMR', 128, 'X300', 100),
        ('Western Digital', 2048, 'CMR', 128, 'WD Black', 80),
        ('Seagate', 8192, 'CMR', 256, 'Exos', 150),
        ('Toshiba', 4096, 'CMR', 256, 'N300', 120);

        INSERT INTO SSD (manufacturer, capacity, max_read_speed, max_write_speed, model, price) VALUES
        ('Samsung', 1024, 3500, 3200, '970 EVO Plus', 150),
        ('Western Digital', 512, 3400, 2900, 'WD Black SN750', 70),
        ('Crucial', 2048, 2400, 1900, 'MX500', 200),
        ('Samsung', 512, 560, 530, '860 EVO', 60),
        ('Western Digital', 1024, 7000, 5300, 'WD Black SN850', 200),
        ('Crucial', 512, 500, 450, 'BX500', 40),
        ('Samsung', 2048, 7000, 5100, '980 PRO', 300),
        ('Western Digital', 256, 3400, 1400, 'WD Blue SN550', 45),
        ('Crucial', 1024, 2100, 1800, 'P5', 110),
        ('Samsung', 4096, 7000, 5000, '990 PRO', 500),
        ('Western Digital', 2048, 3400, 2900, 'WD Blue SN570', 120),
        ('Crucial', 512, 540, 500, 'MX300', 50),
        ('Samsung', 256, 550, 520, '850 EVO', 35),
        ('Western Digital', 1024, 3100, 1600, 'WD Green', 90),
        ('Crucial', 2048, 3500, 3000, 'P3 Plus', 150);

        INSERT INTO motherboard (socket_type, manufacturer, DDR_type, form_factor_type, chipset, memory_slot_num, PCI_Express_ver, M2_port_num, model, price) VALUES
        ('LGA1200', 'ASUS', 'DDR4', 'ATX', 'Z490', 4, '4.0', 2, 'ROG STRIX Z490-E', 250),
        ('AM4', 'MSI', 'DDR4', 'ATX', 'B450', 4, '3.0', 1, 'B450 TOMAHAWK MAX', 130),
        ('TRX40', 'Gigabyte', 'DDR4', 'E-ATX', 'B460', 2, '3.0', 1, 'B460M DS3H', 100),
        ('AM4', 'ASRock', 'DDR4', 'Mini-ITX', 'X570', 2, '4.0', 2, 'X570 Phantom Gaming ITX/TB3', 200),
        ('LGA1200', 'MSI', 'DDR3', 'ATX', 'Z590', 4, '4.0', 3, 'MPG Z590 Gaming Edge WiFi', 300),
        ('TRX40', 'Gigabyte', 'DDR4', 'ATX', 'B550', 4, '4.0', 2, 'B550 AORUS Elite', 180),
        ('LGA1200', 'ASUS', 'DDR3', 'E-ATX', 'H470', 2, '3.0', 1, 'PRIME H470M-PLUS', 120),
        ('AM4', 'MSI', 'DDR4', 'Mini-ITX', 'B550', 2, '4.0', 1, 'MAG B550I Gaming Edge WiFi', 170),
        ('LGA1200', 'Gigabyte', 'DDR4', 'ATX', 'Z590', 4, '4.0', 3, 'Z590 AORUS Ultra', 320),
        ('TRX40', 'ASRock', 'DDR3', 'Micro-ATX', 'B450', 4, '3.0', 1, 'B450M Steel Legend', 90),
        ('LGA1200', 'MSI', 'DDR4', 'ATX', 'Z490', 4, '4.0', 2, 'Z490-A PRO', 180),
        ('AM4', 'ASUS', 'DDR4', 'ATX', 'X570', 4, '4.0', 3, 'ROG Crosshair VIII Hero', 350),
        ('TRX40', 'Gigabyte', 'DDR4', 'Mini-ITX', 'B460', 2, '3.0', 1, 'B460I AORUS PRO AC', 150),
        ('AM4', 'MSI', 'DDR4', 'ATX', 'B450', 4, '3.0', 1, 'B450 GAMING PRO CARBON MAX', 140),
        ('LGA1200', 'ASUS', 'DDR4', 'Micro-ATX', 'H410', 2, '3.0', 1, 'PRIME H410M-K', 80);
    """
    )


def downgrade() -> None:
    op.execute(
        """
    DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
    DROP TABLE IF EXISTS RAM CASCADE;
    DROP TABLE IF EXISTS processor CASCADE;
    DROP TABLE IF EXISTS cooler CASCADE;
    DROP TABLE IF EXISTS computer_case CASCADE;
    DROP TABLE IF EXISTS videocard CASCADE;
    DROP TABLE IF EXISTS power_block CASCADE;
    DROP TABLE IF EXISTS HDD CASCADE;
    DROP TABLE IF EXISTS SSD CASCADE;
    DROP TABLE IF EXISTS motherboard CASCADE;
"""
    )
