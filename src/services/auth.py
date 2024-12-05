from datetime import datetime, timedelta

import bcrypt
from asyncpg import Pool
from fastapi import *
from jose import jwt

from repository.shop import find_shop_by_id, find_shop_by_shopname
from repository.user import create_user, find_user_by_id, find_user_by_username
from schemas import Shop, User
from schemas.user import LoginUserForm, RegisterUserForm

SECRET_KEY = "secretik"
ALGORITHM = "HS256"


def hash_pswd(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


async def register_user(user: RegisterUserForm) -> bool:
    if await find_user_by_username(user.username):
        return False
    else:
        user.password = hash_pswd(user.password)
        await create_user(user)
        return True


async def authenticate_user(username: str, password: str) -> User:
    user = await find_user_by_username(username)
    if not user:
        return None
    if not check_password(password, user.password):
        return None
    return user


async def authenticate_shop(shopname: str, password: str) -> Shop:
    shop = await find_shop_by_shopname(shopname)
    if not shop:
        return None
    if not check_password(password, shop.password):
        return None
    return shop


def create_access_token(id: int, role: str) -> str:
    encode = {"role": role, "id": id}
    expires = datetime.now() + timedelta(days=30)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def validate_access_token_for_user(request: Request) -> bool:
    token = request.cookies.get("access_token")

    if not token:
        return False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False

    role = payload.get("role")
    if role == "admin" or role == "regular_user":
        return True

    return False


def get_user_id_from_token(request: Request) -> int:
    token = request.cookies.get("access_token")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("id")
    return user_id


def validate_access_token_for_shop(request: Request) -> bool:
    token = request.cookies.get("access_token")

    if not token:
        return False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return False

    role = payload.get("role")
    if role == "shop":
        return True

    return False


async def get_current_user(request: Request) -> User:
    token = request.cookies.get("access_token")
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("id")
    user = await find_user_by_id(user_id)
    return user


async def get_current_shop(request: Request) -> Shop:
    token = request.cookies.get("access_token")
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    shop_id = payload.get("id")
    shop = await find_shop_by_id(shop_id)
    return shop


async def get_current_shop(request: Request) -> Shop:
    token = request.cookies.get("access_token")
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    shop_id = payload.get("id")
    shop = await find_user_by_id(shop_id)
    return shop
