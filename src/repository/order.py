from uuid import UUID

from asyncpg import *
from fastapi import *

from repository import admin_connector, shop_connector, user_connector


async def create_new_order(parameters: dict):
    async with user_connector.get_connect() as connection:
        for component in parameters["order"]:
            query = """INSERT INTO orders (user_id, product_id, shop_id, status, product_type, creation_time) VALUES ($1, $2, $3, $4, $5, NOW())"""
            params = (
                parameters["user_id"],
                UUID(parameters["order"][component]),
                int(parameters["shop_id"]),
                "processing",
                component,
            )
            await connection.execute(query, *params)


async def get_user_orders(user_id: int):
    async with shop_connector.get_connect() as connection:
        query = """
            SELECT *
            FROM orders WHERE user_id = $1
        """
        params = user_id
        rows = await connection.fetch(query, params)
        order_dict = {}

        for row in rows:
            order_id = row["order_id"]
            product_type = row["product_type"]
            product_id = str(row["product_id"])

            if order_id not in order_dict:
                order_dict[order_id] = {
                    "shop_id": row["shop_id"],
                    "status": row["status"],
                    "creation_time": row["creation_time"].strftime("%Y-%m-%d %H:%M:%S"),
                    "products": {},
                }

            if row["completion_time"] != None:
                order_dict[order_id]["completion_time"] = row[
                    "completion_time"
                ].strftime("%Y-%m-%d %H:%M:%S")
            else:
                order_dict[order_id]["completion_time"] = row["completion_time"]

            order_dict[order_id]["products"][product_type] = {"product_id": product_id}

        res = [
            {
                "order_id": order_id,
                "shop_id": order["shop_id"],
                "status": order["status"],
                "products": order["products"],
                "creation_time": order["creation_time"],
                "completion_time": order["completion_time"],
            }
            for order_id, order in order_dict.items()
        ]
        return res


async def get_shop_orders(shop_id: int):
    async with user_connector.get_connect() as connection:
        query = """
            SELECT *
            FROM orders WHERE shop_id = $1
        """
        params = shop_id
        rows = await connection.fetch(query, params)
        order_dict = {}

        for row in rows:
            order_id = row["order_id"]
            product_type = row["product_type"]
            product_id = str(row["product_id"])

            if order_id not in order_dict:
                order_dict[order_id] = {
                    "status": row["status"],
                    "creation_time": row["creation_time"].strftime("%Y-%m-%d %H:%M:%S"),
                    "products": {},
                }

            if row["completion_time"] != None:
                order_dict[order_id]["completion_time"] = row[
                    "completion_time"
                ].strftime("%Y-%m-%d %H:%M:%S")
            else:
                order_dict[order_id]["completion_time"] = row["completion_time"]

            order_dict[order_id]["products"][product_type] = {"product_id": product_id}

        res = [
            {
                "order_id": order_id,
                "status": order["status"],
                "products": order["products"],
                "creation_time": order["creation_time"],
                "completion_time": order["completion_time"],
            }
            for order_id, order in order_dict.items()
        ]
        return res


async def update_order_status(order_id: int):
    async with shop_connector.get_connect() as connection:
        query = """
            UPDATE orders SET 
                status = 
                    CASE
                        WHEN status = 'processing' THEN 'accepted'
                        WHEN status = 'accepted' THEN 'ready'
                        WHEN status = 'ready' THEN 'completed'
                        ELSE status
                    END,
                completion_time = 
                    CASE
                        WHEN status = 'ready' THEN NOW()
                        ELSE completion_time
                    END
            WHERE order_id = $1
        """
        await connection.execute(query, order_id)
