from uuid import UUID

from pydantic import BaseModel

__all__ = ["SSD"]


class SSD(BaseModel):
    SSD_id: str
    manufacturer: str
    capacity: int
    max_read_speed: int
    max_write_speed: int
    model: str
    price: int
