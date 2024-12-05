from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import Cooler, LoginUserForm, RegisterUserForm


async def get_all_cooler() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM cooler;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                Cooler(
                    cooler_id=str(row["cooler_id"]),
                    type=row["type"],
                    price=row["price"],
                    model=row["model"],
                ).model_dump()
            )
        return res


async def get_cooler_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT type FROM cooler"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["type"])
        return res


async def get_all_cooler_names():
    coolers = await get_all_cooler()
    res = []
    for cooler in coolers:
        res.append({"cooler_id": str(cooler["cooler_id"]), "name": cooler["model"]})
    return res


async def get_all_cooler_prices():
    coolers = await get_all_cooler()
    res = []
    for cooler in coolers:
        res.append({"cooler_id": str(cooler["cooler_id"]), "price": cooler["price"]})
    return res
