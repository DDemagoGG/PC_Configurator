from uuid import UUID

from pydantic import BaseModel

__all__ = ["PowerBlock"]


class PowerBlock(BaseModel):
    power_block_id: str
    manufacturer: str
    price: int
    power: int
    model: str
