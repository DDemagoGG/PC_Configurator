from pydantic import BaseModel

__all__ = ["LoginShopForm", "Shop"]


class LoginShopForm(BaseModel):
    shopname: str
    password: str


class Shop(BaseModel):
    shopname: str
    password: str
    shop_id: int
    address: str
