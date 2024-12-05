from uuid import UUID

from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import LoginUserForm, Processor, RegisterUserForm


async def get_all_processor() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM processor;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                Processor(
                    cores_num=row["cores_num"],
                    manufacturer=row["manufacturer"],
                    family=row["family"],
                    model=row["model"],
                    frequency=row["frequency"],
                    cash_capacity=row["cash_capacity"],
                    socket_type=row["socket_type"],
                    price=row["price"],
                    processor_id=str(row["processor_id"]),
                ).model_dump()
            )
        return res


async def get_processor_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT manufacturer FROM processor"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["manufacturer"])
        return res


async def get_processor_id_by_socket_type(socket_type: list[str]):
    async with user_connector.get_connect() as connection:
        placeholders = ", ".join(f"${i+1}" for i in range(len(socket_type)))
        query = (
            f"SELECT processor_id FROM processor WHERE socket_type IN ({placeholders})"
        )
        rows = await connection.fetch(query, *socket_type)
        res = []
        for row in rows:
            res.append(str(row["processor_id"]))
        return res


async def get_socket_type_by_id(id: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT socket_type FROM processor WHERE processor_id = $1"""
        rows = await connection.fetch(query, (UUID(id)))
        for row in rows:
            return row["socket_type"]


async def get_all_processor_names():
    processors = await get_all_processor()
    res = []
    for processor in processors:
        res.append(
            {
                "processor_id": str(processor["processor_id"]),
                "name": (
                    processor["manufacturer"]
                    + " "
                    + processor["family"]
                    + " "
                    + processor["model"]
                ),
            }
        )
    return res


async def get_all_processor_prices():
    processors = await get_all_processor()
    res = []
    for processor in processors:
        res.append(
            {
                "processor_id": str(processor["processor_id"]),
                "price": processor["price"],
            }
        )
    return res
