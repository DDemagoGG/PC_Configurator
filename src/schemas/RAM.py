from uuid import UUID

from pydantic import BaseModel

__all__ = ["RAM"]


class RAM(BaseModel):
    RAM_id: str
    manufacturer: str
    model: str
    capacity: int
    DDR_type: str
    frequency: int
    price: int
