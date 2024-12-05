from uuid import UUID

from pydantic import BaseModel

__all__ = ["Videocard"]


class Videocard(BaseModel):
    videocard_id: str
    manufacturer: str
    videomemory_capacity: int
    memory_bus_width: int
    memory_type: str
    PCI_Express_ver: str
    model: str
    price: int
