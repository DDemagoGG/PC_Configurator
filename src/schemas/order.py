from datetime import datetime

from pydantic import BaseModel
from typing import Optional


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

class NearlyOrder(BaseModel):
    motherboard: Optional[str] = None
    processor: Optional[str] = None
    RAM: Optional[str] = None
    SSD: Optional[str] = None
    HDD: Optional[str] = None
    computer_case: Optional[str] = None
    videocard: Optional[str] = None
    power_block: Optional[str] = None
    cooler: Optional[str] = None


class CreateOrderForm(BaseModel):
    order: Order
    shop_id: str
