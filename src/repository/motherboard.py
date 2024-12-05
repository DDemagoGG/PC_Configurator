from typing import List
from uuid import UUID

from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector
from schemas import LoginUserForm, Motherboard, RegisterUserForm


async def get_all_motherboard() -> List[dict]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM motherboard;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(
                Motherboard(
                    motherboard_id=str(row["motherboard_id"]),
                    socket_type=row["socket_type"],
                    manufacturer=row["manufacturer"],
                    DDR_type=row["ddr_type"],
                    form_factor_type=row["form_factor_type"],
                    chipset=row["chipset"],
                    memory_slot_num=row["memory_slot_num"],
                    PCI_Express_ver=row["pci_express_ver"],
                    M2_port_num=row["m2_port_num"],
                    model=row["model"],
                    price=row["price"],
                ).model_dump()
            )
        return res


async def get_motherboard_group_parameters() -> List[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT manufacturer FROM motherboard"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append(row["manufacturer"])
        return res


async def get_motherboard_by_id(id: str) -> Motherboard:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM motherboard WHERE motherboard_id = $1"""
        rows = await connection.fetch(query, UUID(id))
        if rows:
            return Motherboard(
                motherboard_id=str(rows[0]["motherboard_id"]),
                socket_type=rows[0]["socket_type"],
                manufacturer=rows[0]["manufacturer"],
                DDR_type=rows[0]["ddr_type"],
                form_factor_type=rows[0]["form_factor_type"],
                chipset=rows[0]["chipset"],
                memory_slot_num=rows[0]["memory_slot_num"],
                PCI_Express_ver=rows[0]["pci_express_ver"],
                M2_port_num=rows[0]["m2_port_num"],
                model=rows[0]["model"],
                price=rows[0]["price"],
            )
        return None


async def get_compatibilities_by_motherboard_id(id: str):
    motherboard = await get_motherboard_by_id(id)
    return {
        "DDR_type": [motherboard.DDR_type],
        "form_factor_type": [motherboard.form_factor_type],
        "PCI_Express_ver": [motherboard.PCI_Express_ver],
        "socket_type": [motherboard.socket_type],
    }


async def get_motherboard_id_by_compatibilities(
    socket_type: str, DDR_type: str, form_factor_type: str, PCI_Express_ver: str
) -> List[str]:
    async with user_connector.get_connect() as connection:
        query = """SELECT * FROM motherboard WHERE socket_type = $1 AND DDR_type = $2 AND form_factor_type = $3 AND PCI_Express_ver = $4"""
        rows = await connection.fetch(
            query, (socket_type, DDR_type, form_factor_type, PCI_Express_ver)
        )
        res = []
        for row in rows:
            res.append(str(row["motherboad_id"]))
        return res


async def get_motherboard_id_by_socket_type(socket_type: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT motherboard_id FROM motherboard WHERE socket_type = $1"""
        rows = await connection.fetch(query, (socket_type))
        ids = []
        for row in rows:
            ids.append(str(row["motherboard_id"]))
        return ids


async def get_motherboard_id_by_DDR_type(DDR_type: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT motherboard_id FROM motherboard WHERE DDR_type = $1"""
        rows = await connection.fetch(query, (DDR_type))
        ids = []
        for row in rows:
            ids.append(str(row["motherboard_id"]))
        return ids


async def get_motherboard_id_by_form_factor(form_factor_type: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT motherboard_id FROM motherboard WHERE form_factor_type = $1"""
        rows = await connection.fetch(query, (form_factor_type))
        ids = []
        for row in rows:
            ids.append(str(row["motherboard_id"]))
        return ids


async def get_motherboard_id_by_PCI_Express_ver(PCI_Express_ver: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT motherboard_id FROM motherboard WHERE PCI_Express_ver = $1"""
        rows = await connection.fetch(query, (PCI_Express_ver))
        ids = []
        for row in rows:
            ids.append(str(row["motherboard_id"]))
        return ids


async def get_compatibilities_by_socket_type(socket_type: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT DDR_type FROM motherboard WHERE socket_type = $1"""
        rows = await connection.fetch(query, (socket_type))
        ddr_types = []
        for row in rows:
            ddr_types.append(row["ddr_type"])

        query = """SELECT DISTINCT form_factor_type FROM motherboard WHERE socket_type = $1"""
        rows = await connection.fetch(query, (socket_type))
        form_factors = []
        for row in rows:
            form_factors.append(row["form_factor_type"])

        query = """SELECT DISTINCT PCI_Express_ver FROM motherboard WHERE socket_type = $1"""
        rows = await connection.fetch(query, (socket_type))
        pci_express_vers = []
        for row in rows:
            pci_express_vers.append(row["pci_express_ver"])
        return {
            "DDR_type": ddr_types,
            "form_factor_type": form_factors,
            "PCI_Express_ver": pci_express_vers,
        }


async def get_compatibilities_by_ddr_type(ddr_type: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT socket_type FROM motherboard WHERE DDR_type = $1"""
        rows = await connection.fetch(query, (ddr_type))
        socket_types = []
        for row in rows:
            socket_types.append(row["socket_type"])

        query = (
            """SELECT DISTINCT form_factor_type FROM motherboard WHERE DDR_type = $1"""
        )
        rows = await connection.fetch(query, (ddr_type))
        form_factors = []
        for row in rows:
            form_factors.append(row["form_factor_type"])

        query = (
            """SELECT DISTINCT PCI_Express_ver FROM motherboard WHERE DDR_type = $1"""
        )
        rows = await connection.fetch(query, (ddr_type))
        pci_express_vers = []
        for row in rows:
            pci_express_vers.append(row["pci_express_ver"])
        return {
            "socket_type": socket_types,
            "form_factor_type": form_factors,
            "PCI_Express_ver": pci_express_vers,
        }


async def get_compatibilities_by_form_factor(form_factor_type: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT socket_type FROM motherboard WHERE form_factor_type = $1"""
        rows = await connection.fetch(query, (form_factor_type))
        socket_types = []
        for row in rows:
            socket_types.append(row["socket_type"])

        query = (
            """SELECT DISTINCT DDR_type FROM motherboard WHERE form_factor_type = $1"""
        )
        rows = await connection.fetch(query, (form_factor_type))
        ddr_types = []
        for row in rows:
            ddr_types.append(row["ddr_type"])

        query = """SELECT DISTINCT PCI_Express_ver FROM motherboard WHERE form_factor_type = $1"""
        rows = await connection.fetch(query, (form_factor_type))
        pci_express_vers = []
        for row in rows:
            pci_express_vers.append(row["pci_express_ver"])
        return {
            "socket_type": socket_types,
            "DDR_type": ddr_types,
            "PCI_Express_ver": pci_express_vers,
        }


async def get_compatibilities_by_pci(pci: str):
    async with user_connector.get_connect() as connection:
        query = """SELECT DISTINCT socket_type FROM motherboard WHERE PCI_Express_ver = $1"""
        rows = await connection.fetch(query, (pci))
        socket_types = []
        for row in rows:
            socket_types.append(row["socket_type"])

        query = (
            """SELECT DISTINCT DDR_type FROM motherboard WHERE PCI_Express_ver = $1"""
        )
        rows = await connection.fetch(query, (pci))
        ddr_types = []
        for row in rows:
            ddr_types.append(row["ddr_type"])

        query = """SELECT DISTINCT form_factor_type FROM motherboard WHERE PCI_Express_ver = $1"""
        rows = await connection.fetch(query, (pci))
        form_factors = []
        for row in rows:
            form_factors.append(row["form_factor_type"])
        return {
            "socket_type": socket_types,
            "DDR_type": ddr_types,
            "form_factor_type": form_factors,
        }


async def get_all_motherboard_names():
    motherboards = await get_all_motherboard()
    res = []
    for motherboard in motherboards:
        res.append(
            {
                "motherboard_id": str(motherboard["motherboard_id"]),
                "name": (motherboard["manufacturer"] + " " + motherboard["model"]),
            }
        )
    return res


async def get_all_motherboard_prices():
    motherboards = await get_all_motherboard()
    res = []
    for motherboard in motherboards:
        res.append(
            {
                "motherboard_id": str(motherboard["motherboard_id"]),
                "price": motherboard["price"],
            }
        )
    return res
