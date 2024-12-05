from asyncpg import *
from fastapi import *

from repository import admin_connector, user_connector
from schemas import LoginUserForm, RegisterUserForm, User


async def create_user(user: RegisterUserForm):
    async with user_connector.get_connect() as connection:
        query = """
            INSERT INTO users (username, password, email, birthdate, role)
            VALUES ($1, $2, $3, $4, $5)
        """
        params = (
            user.username,
            user.password,
            user.email,
            user.birthdate,
            "regular_user",
        )
        await connection.execute(query, *params)


async def find_user_by_username(username: str) -> User:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM users WHERE username=$1;"""
        params = username
        rows = await connection.fetch(query, params)
        if rows:
            return User(
                username=rows[0]["username"],
                password=rows[0]["password"],
                email=rows[0]["email"],
                birthdate=rows[0]["birthdate"],
                user_id=rows[0]["user_id"],
                role=rows[0]["role"],
            )
        return None


async def find_user_by_id(user_id: int) -> User:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM users WHERE user_id=$1;"""
        params = user_id
        rows = await connection.fetch(query, params)
        if rows:
            return User(
                username=rows[0]["username"],
                password=rows[0]["password"],
                email=rows[0]["email"],
                birthdate=rows[0]["birthdate"],
                user_id=rows[0]["user_id"],
                role=rows[0]["role"],
            )
        return None


# async def get_user_password(user: LoginUserForm):
