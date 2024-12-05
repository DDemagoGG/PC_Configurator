from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import SSD, LoginUserForm, RegisterUserForm


async def get_all_ssd() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM SSD;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                SSD(
                    SSD_id=str(row["ssd_id"]),
                    manufacturer=row["manufacturer"],
                    capacity=row["capacity"],
                    max_read_speed=row["max_read_speed"],
                    max_write_speed=row["max_write_speed"],
                    model=row["model"],
                    price=row["price"],
                ).model_dump()
            )
        return res


async def get_SSD_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT capacity FROM SSD ORDER BY capacity"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["capacity"])
        return res


async def get_all_SSD_names():
    ssds = await get_all_ssd()
    res = []
    for ssd in ssds:
        res.append(
            {
                "SSD_id": str(ssd["SSD_id"]),
                "name": (
                    ssd["manufacturer"]
                    + " "
                    + ssd["model"]
                    + " "
                    + str(ssd["capacity"])
                    + " MB"
                ),
            }
        )
    return res


async def get_all_SSD_prices():
    ssds = await get_all_ssd()
    res = []
    for ssd in ssds:
        res.append({"SSD_id": str(ssd["SSD_id"]), "price": ssd["price"]})
    return res
