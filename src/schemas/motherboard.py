from uuid import UUID

from pydantic import BaseModel

__all__ = ["Motherboard"]


class Motherboard(BaseModel):
    motherboard_id: str
    socket_type: str
    manufacturer: str
    DDR_type: str
    form_factor_type: str
    chipset: str
    memory_slot_num: int
    PCI_Express_ver: str
    M2_port_num: int
    model: str
    price: int
