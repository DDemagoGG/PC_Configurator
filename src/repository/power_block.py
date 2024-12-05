from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import LoginUserForm, PowerBlock, RegisterUserForm


async def get_all_power_block() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM power_block;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                PowerBlock(
                    power_block_id=str(row["power_block_id"]),
                    manufacturer=row["manufacturer"],
                    price=row["price"],
                    power=row["power"],
                    model=row["model"],
                ).model_dump()
            )
        return res


async def get_power_block_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT power FROM power_block ORDER BY power"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["power"])
        return res


async def get_all_power_block_names():
    power_blocks = await get_all_power_block()
    res = []
    for power_block in power_blocks:
        res.append(
            {
                "power_block_id": str(power_block["power_block_id"]),
                "name": (power_block["manufacturer"] + " " + power_block["model"]),
            }
        )
    return res


async def get_all_power_block_prices():
    power_blocks = await get_all_power_block()
    res = []
    for power_block in power_blocks:
        res.append(
            {
                "power_block_id": str(power_block["power_block_id"]),
                "price": power_block["price"],
            }
        )
    return res
