from datetime import datetime

from fastapi import *

from repository.computer_case import get_all_computer_case_prices
from repository.cooler import get_all_cooler_prices
from repository.HDD import get_all_HDD_prices
from repository.motherboard import get_all_motherboard_prices
from repository.order import get_shop_orders, update_order_status
from repository.power_block import get_all_power_block_prices
from repository.processor import get_all_processor_prices
from repository.RAM import get_all_RAM_prices
from repository.shop import find_shop_by_id, get_all_shops
from repository.SSD import get_all_SSD_prices
from repository.videocard import get_all_videocard_prices
from services.home import get_all_names


async def get_all_prices():
    rams = await get_all_RAM_prices()
    processors = await get_all_processor_prices()
    coolers = await get_all_cooler_prices()
    computer_cases = await get_all_computer_case_prices()
    videocards = await get_all_videocard_prices()
    power_blocks = await get_all_power_block_prices()
    hdds = await get_all_HDD_prices()
    ssds = await get_all_SSD_prices()
    motherboards = await get_all_motherboard_prices()
    return {
        "RAM": rams,
        "processor": processors,
        "cooler": coolers,
        "computer_case": computer_cases,
        "videocard": videocards,
        "power_block": power_blocks,
        "HDD": hdds,
        "SSD": ssds,
        "motherboard": motherboards,
    }


async def get_parameters(shop_id: int):
    orders = await get_shop_orders(shop_id)
    names = await get_all_names()
    prices = await get_all_prices()
    for order in orders:
        total_price = 0
        products = order["products"]
        for product_type in products:
            product_names = names[product_type]
            product_prices = prices[product_type]
            for product_name in product_names:
                if (
                    product_name[product_type + "_id"]
                    == products[product_type]["product_id"]
                ):
                    products[product_type]["product_name"] = product_name["name"]
                    break
            for product_price in product_prices:
                if (
                    product_price[product_type + "_id"]
                    == products[product_type]["product_id"]
                ):
                    products[product_type]["product_price"] = product_price["price"]
                    total_price += product_price["price"]
                    break
        order["total_price"] = total_price
    return {"orders": orders}


async def update_order(order_id: int):
    await update_order_status(order_id)
