from asyncpg import *
from fastapi import *

from repository import shop_connector
from schemas import LoginShopForm, Shop


async def find_shop_by_shopname(shopname: str) -> Shop:
    async with shop_connector.get_connect() as connection:
        query = """SELECT * FROM shops WHERE shopname=$1;"""
        params = shopname
        rows = await connection.fetch(query, params)
        if rows:
            return Shop(
                shopname=rows[0]["shopname"],
                password=rows[0]["password"],
                shop_id=rows[0]["shop_id"],
                address=rows[0]["address"],
            )
        return None


async def find_shop_by_id(shop_id: int) -> Shop:
    async with shop_connector.get_connect() as connection:
        query = """SELECT * FROM shops WHERE shop_id=$1;"""
        params = shop_id
        rows = await connection.fetch(query, params)
        if rows:
            return Shop(
                shopname=rows[0]["shopname"],
                password=rows[0]["password"],
                shop_id=rows[0]["shop_id"],
                address=rows[0]["address"],
            )
        return None


async def get_all_shops():
    async with shop_connector.get_connect() as connection:
        query = """SELECT * FROM shops;"""
        rows = await connection.fetch(query)
        res = []
        for row in rows:
            res.append({"shop_id": row["shop_id"], "address": row["address"]})
        return res
