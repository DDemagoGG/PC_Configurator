import json
from datetime import datetime, timedelta

from fastapi import *
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from services.auth import get_user_id_from_token, validate_access_token_for_shop
from services.shophome import get_parameters, update_order

router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.get("/shop/home", response_class=responses.HTMLResponse)
async def show_home_page(request: Request):
    if validate_access_token_for_shop(request):
        shop_id = get_user_id_from_token(request)
        params = await get_parameters(shop_id)
        params["request"] = request
        return template.TemplateResponse("ShopHomepage.html", params)
    return RedirectResponse(url="/shop/login", status_code=status.HTTP_302_FOUND)


@router.patch("/shop/home")
async def update_order_status_handler(order_id: int):
    await update_order(order_id)
    response = Response(status_code=status.HTTP_200_OK)
    return response
