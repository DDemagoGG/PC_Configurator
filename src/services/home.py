from datetime import datetime, timedelta

import bcrypt
from asyncpg import Pool
from fastapi import *
from jose import jwt

from repository.computer_case import (
    get_all_computer_case,
    get_all_computer_case_names,
    get_computer_case_group_parameters,
    get_computer_case_id_by_form_factor,
    get_form_factor_by_id,
)
from repository.cooler import (
    get_all_cooler,
    get_all_cooler_names,
    get_cooler_group_parameters,
)
from repository.HDD import get_all_hdd, get_all_HDD_names, get_HDD_group_parameters
from repository.motherboard import (
    get_all_motherboard,
    get_all_motherboard_names,
    get_compatibilities_by_ddr_type,
    get_compatibilities_by_form_factor,
    get_compatibilities_by_motherboard_id,
    get_compatibilities_by_pci,
    get_compatibilities_by_socket_type,
    get_motherboard_group_parameters,
    get_motherboard_id_by_DDR_type,
    get_motherboard_id_by_form_factor,
    get_motherboard_id_by_PCI_Express_ver,
    get_motherboard_id_by_socket_type,
)
from repository.power_block import (
    get_all_power_block,
    get_all_power_block_names,
    get_power_block_group_parameters,
)
from repository.processor import (
    get_all_processor,
    get_all_processor_names,
    get_processor_group_parameters,
    get_processor_id_by_socket_type,
    get_socket_type_by_id,
)
from repository.RAM import (
    get_all_RAM,
    get_all_ram_names,
    get_DDR_type_by_id,
    get_RAM_group_parameters,
    get_RAM_id_by_DDR_type,
)
from repository.SSD import get_all_ssd, get_all_SSD_names, get_SSD_group_parameters
from repository.videocard import (
    get_all_videocard,
    get_all_videocard_names,
    get_PCI_Express_ver_by_id,
    get_videocard_group_parameters,
    get_videocard_id_by_PCI_Express_ver,
)
from schemas import Shop, User


async def get_all_group_parameters() -> dict:
    processor_parameters = await get_processor_group_parameters()
    motherboard_parameters = await get_motherboard_group_parameters()
    computer_case_parameters = await get_computer_case_group_parameters()
    ram_parameters = await get_RAM_group_parameters()
    videocard_parameters = await get_videocard_group_parameters()
    hdd_parameters = await get_HDD_group_parameters()
    ssd_parameters = await get_SSD_group_parameters()
    power_block_parameters = await get_power_block_group_parameters()
    cooler_parameters = await get_cooler_group_parameters()
    return {
        "processor_groups": processor_parameters,
        "motherboard_groups": motherboard_parameters,
        "computer_case_groups": computer_case_parameters,
        "RAM_groups": ram_parameters,
        "videocard_groups": videocard_parameters,
        "HDD_groups": hdd_parameters,
        "SSD_groups": ssd_parameters,
        "power_block_groups": power_block_parameters,
        "cooler_groups": cooler_parameters,
    }


async def get_all_components() -> dict:
    processors = await get_all_processor()
    motherboards = await get_all_motherboard()
    computer_cases = await get_all_computer_case()
    rams = await get_all_RAM()
    videocards = await get_all_videocard()
    hdds = await get_all_hdd()
    ssds = await get_all_ssd()
    power_blocks = await get_all_power_block()
    coolers = await get_all_cooler()
    return {
        "processor": processors,
        "motherboard": motherboards,
        "computer_case": computer_cases,
        "RAM": rams,
        "videocard": videocards,
        "HDD": hdds,
        "SSD": ssds,
        "power_block": power_blocks,
        "cooler": coolers,
    }


async def get_components_by_applied_processor(id: str):
    socket_type = await get_socket_type_by_id(id)
    motherboards = await get_motherboard_id_by_socket_type(socket_type)
    compatibilities = await get_compatibilities_by_socket_type(socket_type)
    computer_cases = await get_computer_case_id_by_form_factor(
        compatibilities["form_factor_type"]
    )
    videocards = await get_videocard_id_by_PCI_Express_ver(
        compatibilities["PCI_Express_ver"]
    )
    rams = await get_RAM_id_by_DDR_type(compatibilities["DDR_type"])
    return {
        "motherboard": motherboards,
        "computer_case": computer_cases,
        "videocard": videocards,
        "RAM": rams,
    }


async def get_components_by_applied_RAM(id: str):
    DDR_type = await get_DDR_type_by_id(id)
    motherboards = await get_motherboard_id_by_DDR_type(DDR_type)
    compatibilities = await get_compatibilities_by_ddr_type(DDR_type)
    computer_cases = await get_computer_case_id_by_form_factor(
        compatibilities["form_factor_type"]
    )
    videocards = await get_videocard_id_by_PCI_Express_ver(
        compatibilities["PCI_Express_ver"]
    )
    processors = await get_processor_id_by_socket_type(compatibilities["socket_type"])
    return {
        "motherboard": motherboards,
        "computer_case": computer_cases,
        "videocard": videocards,
        "processor": processors,
    }


async def get_components_by_applied_computer_case(id: str):
    form_factor = await get_form_factor_by_id(id)
    motherboards = await get_motherboard_id_by_form_factor(form_factor)
    compatibilities = await get_compatibilities_by_form_factor(form_factor)
    videocards = await get_videocard_id_by_PCI_Express_ver(
        compatibilities["PCI_Express_ver"]
    )
    processors = await get_processor_id_by_socket_type(compatibilities["socket_type"])
    rams = await get_RAM_id_by_DDR_type(compatibilities["DDR_type"])
    return {
        "motherboard": motherboards,
        "RAM": rams,
        "videocard": videocards,
        "processor": processors,
    }


async def get_components_by_applied_videocard(id: str):
    pci = await get_PCI_Express_ver_by_id(id)
    motherboards = await get_motherboard_id_by_PCI_Express_ver(pci)
    compatibilities = await get_compatibilities_by_pci(pci)
    processors = await get_processor_id_by_socket_type(compatibilities["socket_type"])
    rams = await get_RAM_id_by_DDR_type(compatibilities["DDR_type"])
    computer_cases = await get_computer_case_id_by_form_factor(
        compatibilities["form_factor_type"]
    )
    return {
        "motherboard": motherboards,
        "RAM": rams,
        "computer_case": computer_cases,
        "processor": processors,
    }


async def get_components_by_applied_motherboard(id: str):
    compatibilities = await get_compatibilities_by_motherboard_id(id)
    processors = await get_processor_id_by_socket_type(compatibilities["socket_type"])
    videocards = await get_videocard_id_by_PCI_Express_ver(
        compatibilities["PCI_Express_ver"]
    )
    computer_cases = await get_computer_case_id_by_form_factor(
        compatibilities["form_factor_type"]
    )
    rams = await get_RAM_id_by_DDR_type(compatibilities["DDR_type"])
    return {
        "processor": processors,
        "videocard": videocards,
        "computer_case": computer_cases,
        "RAM": rams,
    }


async def get_all_names():
    rams = await get_all_ram_names()
    processors = await get_all_processor_names()
    coolers = await get_all_cooler_names()
    computer_cases = await get_all_computer_case_names()
    videocards = await get_all_videocard_names()
    power_blocks = await get_all_power_block_names()
    hdds = await get_all_HDD_names()
    ssds = await get_all_SSD_names()
    motherboards = await get_all_motherboard_names()
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
