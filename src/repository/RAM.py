from uuid import UUID

from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import RAM, LoginUserForm, RegisterUserForm


async def get_all_RAM() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM RAM;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                RAM(
                    RAM_id=str(row["ram_id"]),
                    manufacturer=row["manufacturer"],
                    model=row["model"],
                    capacity=row["capacity"],
                    DDR_type=row["ddr_type"],
                    frequency=row["frequency"],
                    price=row["price"],
                ).model_dump()
            )
        return res


async def get_RAM_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT manufacturer FROM RAM"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["manufacturer"])
        return res


async def get_RAM_id_by_DDR_type(DDR_type: list[str]):
    async with user_connector.get_connect() as connection:
        placeholders = ", ".join(f"${i+1}" for i in range(len(DDR_type)))
        query = f"SELECT RAM_id FROM RAM WHERE DDR_type IN ({placeholders})"
        rows = await connection.fetch(query, *DDR_type)
        res = []
        for row in rows:
            res.append(str(row["ram_id"]))
        return res


async def get_DDR_type_by_id(id: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT DDR_type FROM RAM WHERE RAM_id = $1"""
        rows = await connection.fetch(query, (UUID(id)))
        for row in rows:
            return row["ddr_type"]


async def get_all_ram_names():
    rams = await get_all_RAM()
    res = []
    for ram in rams:
        res.append(
            {
                "RAM_id": str(ram["RAM_id"]),
                "name": (
                    ram["manufacturer"]
                    + " "
                    + ram["model"]
                    + " "
                    + str(ram["capacity"])
                    + " GB"
                ),
            }
        )
    return res


async def get_all_RAM_prices():
    rams = await get_all_RAM()
    res = []
    for ram in rams:
        res.append({"RAM_id": str(ram["RAM_id"]), "price": ram["price"]})
    return res
