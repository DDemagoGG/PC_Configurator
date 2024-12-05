from datetime import datetime

from fastapi import *

from repository.order import create_new_order
from repository.shop import find_shop_by_id, get_all_shops


async def get_parameters():
    shops = await get_all_shops()
    return shops


async def create_order(order: dict, shop_id: int, user_id: int):
    parameters = {"order": order}
    parameters["shop_id"] = shop_id
    parameters["user_id"] = user_id
    await create_new_order(parameters)
