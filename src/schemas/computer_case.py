from uuid import UUID

from pydantic import BaseModel

__all__ = ["ComputerCase"]


class ComputerCase(BaseModel):
    computer_case_id: str
    price: int
    manufacturer: str
    form_factor_type: str
    model: str
    tower_size: str
    main_color: str
