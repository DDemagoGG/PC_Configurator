from uuid import UUID

from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import ComputerCase, LoginUserForm, RegisterUserForm


async def get_all_computer_case() -> list[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM computer_case;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                ComputerCase(
                    computer_case_id=str(row["computer_case_id"]),
                    price=row["price"],
                    manufacturer=row["manufacturer"],
                    form_factor_type=row["form_factor_type"],
                    model=row["model"],
                    tower_size=row["tower_size"],
                    main_color=row["main_color"],
                ).model_dump()
            )
        return res


async def get_computer_case_group_parameters() -> list[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT manufacturer FROM computer_case"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["manufacturer"])
        return res


async def get_computer_case_id_by_form_factor(form_factor: list[str]):
    async with user_connector.get_connect() as connection:
        placeholders = ", ".join(f"${i+1}" for i in range(len(form_factor)))
        query = f"SELECT computer_case_id FROM computer_case WHERE form_factor_type IN ({placeholders})"
        rows = await connection.fetch(query, *form_factor)
        res = []
        for row in rows:
            res.append(str(row["computer_case_id"]))
        return res


async def get_form_factor_by_id(id: str):
    async with user_connector.get_connect() as connection:
        query = (
            """SELECT form_factor_type FROM computer_case WHERE computer_case_id = $1"""
        )
        rows = await connection.fetch(query, (UUID(id)))
        for row in rows:
            return row["form_factor_type"]


async def get_all_computer_case_names():
    computer_cases = await get_all_computer_case()
    res = []
    for computer_case in computer_cases:
        res.append(
            {
                "computer_case_id": str(computer_case["computer_case_id"]),
                "name": (computer_case["manufacturer"] + " " + computer_case["model"]),
            }
        )
    return res


async def get_all_computer_case_prices():
    computer_cases = await get_all_computer_case()
    res = []
    for computer_case in computer_cases:
        res.append(
            {
                "computer_case_id": str(computer_case["computer_case_id"]),
                "price": computer_case["price"],
            }
        )
    return res
