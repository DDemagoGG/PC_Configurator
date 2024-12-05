from uuid import UUID

from pydantic import BaseModel

__all__ = ["Cooler"]


class Cooler(BaseModel):
    cooler_id: str
    type: str
    price: int
    model: str
