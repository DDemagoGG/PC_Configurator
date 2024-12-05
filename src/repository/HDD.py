from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import HDD, LoginUserForm, RegisterUserForm


async def get_all_hdd() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM HDD;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                HDD(
                    HDD_id=str(row["hdd_id"]),
                    manufacturer=row["manufacturer"],
                    capacity=row["capacity"],
                    recording_technology=row["recording_technology"],
                    cash_capacity=row["cash_capacity"],
                    model=row["model"],
                    price=row["price"],
                ).model_dump()
            )
        return res


async def get_HDD_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT capacity FROM HDD ORDER BY capacity"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["capacity"])
        return res


async def get_all_HDD_names():
    hdds = await get_all_hdd()
    res = []
    for hdd in hdds:
        res.append(
            {
                "HDD_id": str(hdd["HDD_id"]),
                "name": (
                    hdd["manufacturer"]
                    + " "
                    + hdd["model"]
                    + " "
                    + str(hdd["capacity"])
                    + " MB"
                ),
            }
        )
    return res


async def get_all_HDD_prices():
    hdds = await get_all_hdd()
    res = []
    for hdd in hdds:
        res.append({"HDD_id": str(hdd["HDD_id"]), "price": hdd["price"]})
    return res
