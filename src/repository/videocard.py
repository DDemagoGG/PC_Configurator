from uuid import UUID

from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import LoginUserForm, RegisterUserForm, Videocard


async def get_all_videocard() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM videocard;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                Videocard(
                    videocard_id=str(row["videocard_id"]),
                    manufacturer=row["manufacturer"],
                    videomemory_capacity=row["videomemory_capacity"],
                    memory_bus_width=row["memory_bus_width"],
                    memory_type=row["memory_type"],
                    PCI_Express_ver=row["pci_express_ver"],
                    model=row["model"],
                    price=row["price"],
                ).model_dump()
            )
        return res


async def get_videocard_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT manufacturer FROM videocard"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["manufacturer"])
        return res


async def get_videocard_id_by_PCI_Express_ver(PCI_Express_ver: list[str]):
    async with user_connector.get_connect() as connection:
        placeholders = ", ".join(f"${i+1}" for i in range(len(PCI_Express_ver)))
        query = f"SELECT videocard_id FROM videocard WHERE PCI_Express_ver IN ({placeholders})"
        rows = await connection.fetch(query, *PCI_Express_ver)
        res = []
        for row in rows:
            res.append(str(row["videocard_id"]))
        return res


async def get_PCI_Express_ver_by_id(id: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT PCI_Express_ver FROM videocard WHERE videocard_id = $1"""
        rows = await connection.fetch(query, (UUID(id)))
        for row in rows:
            return row["pci_express_ver"]


async def get_all_videocard_names():
    videocards = await get_all_videocard()
    res = []
    for videocard in videocards:
        res.append(
            {
                "videocard_id": str(videocard["videocard_id"]),
                "name": (videocard["manufacturer"] + " " + videocard["model"]),
            }
        )
    return res


async def get_all_videocard_prices():
    videocards = await get_all_videocard()
    res = []
    for videocard in videocards:
        res.append(
            {
                "videocard_id": str(videocard["videocard_id"]),
                "price": videocard["price"],
            }
        )
    return res
