from datetime import date

from pydantic import BaseModel

__all__ = ["LoginUserForm", "RegisterUserForm", "User"]


class LoginUserForm(BaseModel):
    username: str
    password: str


class RegisterUserForm(BaseModel):
    username: str
    email: str
    password: str
    birthdate: date


class User(BaseModel):
    username: str
    password: str
    email: str
    birthdate: date
    user_id: int
    role: str
