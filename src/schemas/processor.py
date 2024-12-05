from uuid import UUID

from pydantic import BaseModel

__all__ = ["Processor"]


class Processor(BaseModel):
    processor_id: str
    cores_num: int
    manufacturer: str
    family: str
    model: str
    frequency: float
    cash_capacity: int
    socket_type: str
    price: int
