from uuid import UUID

from pydantic import BaseModel

__all__ = ["HDD"]


class HDD(BaseModel):
    HDD_id: str
    manufacturer: str
    capacity: int
    recording_technology: str
    cash_capacity: int
    model: str
    price: int
