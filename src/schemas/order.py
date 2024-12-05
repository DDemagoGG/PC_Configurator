from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    motherboard: str
    processor: str
    RAM: str
    SSD: str
    HDD: str
    computer_case: str
    videocard: str
    power_block: str
    cooler: str


class CreateOrderForm(BaseModel):
    order: Order
    shop_id: str
