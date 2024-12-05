import json
from datetime import datetime, timedelta

from fastapi import *
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from schemas.shop import LoginShopForm
from schemas.user import LoginUserForm, RegisterUserForm
from services.auth import (
    authenticate_shop,
    authenticate_user,
    create_access_token,
    get_current_user,
    register_user,
    validate_access_token_for_user,
)
from services.home import (
    get_all_components,
    get_all_group_parameters,
    get_all_names,
    get_components_by_applied_computer_case,
    get_components_by_applied_motherboard,
    get_components_by_applied_processor,
    get_components_by_applied_RAM,
    get_components_by_applied_videocard,
)

router = APIRouter(tags=["Homepage"])

template = Jinja2Templates(directory="templates")


@router.get("/user/home", response_class=responses.HTMLResponse)
async def show_home_page(request: Request):
    if validate_access_token_for_user(request):
        params = {"request": request}
        params["group_parameters"] = await get_all_group_parameters()
        params["components"] = await get_all_components()
        params["names"] = await get_all_names()
        return template.TemplateResponse("UserHomepage.html", params)
    return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)


@router.get("/api/processor")
async def apply_processor(id: str):
    components = await get_components_by_applied_processor(id)
    return Response(
        status_code=status.HTTP_200_OK, content=json.dumps(components, indent=4)
    )


@router.get("/api/motherboard")
async def apply_motherboard(id: str):
    components = await get_components_by_applied_motherboard(id)
    return Response(
        status_code=status.HTTP_200_OK, content=json.dumps(components, indent=4)
    )


@router.get("/api/computer_case")
async def apply_computer_case(id: str):
    components = await get_components_by_applied_computer_case(id)
    return Response(
        status_code=status.HTTP_200_OK, content=json.dumps(components, indent=4)
    )


@router.get("/api/videocard")
async def apply_videocard(id: str):
    components = await get_components_by_applied_videocard(id)
    return Response(
        status_code=status.HTTP_200_OK, content=json.dumps(components, indent=4)
    )


@router.get("/api/RAM")
async def apply_RAM(id: str):
    components = await get_components_by_applied_RAM(id)
    return Response(
        status_code=status.HTTP_200_OK, content=json.dumps(components, indent=4)
    )
