import json
from datetime import datetime, timedelta

from fastapi import *
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from services.auth import get_user_id_from_token, validate_access_token_for_shop
from services.shophome import get_parameters, update_order

from repository.redis import redis_client
from repository.order import get_shop_orders, get_order


router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.get("/shop/home", response_class=responses.HTMLResponse)
async def show_home_page(request: Request):
    if validate_access_token_for_shop(request):
        shop_id = get_user_id_from_token(request)
        token = request.cookies.get("access_token")
        redis_token = redis_client.get(f"auth_shop_token:{shop_id}")
        if redis_token == token:
            params = await get_parameters(shop_id)
            params["request"] = request
            return template.TemplateResponse("ShopHomepage.html", params)
    return RedirectResponse(url="/shop/login", status_code=status.HTTP_302_FOUND)


@router.patch("/shop/home")
async def update_order_status_handler(order_id: int):
    await update_order(order_id)
    order = await get_order(order_id)
    redis_client.publish(
        'order:status-changed',
        json.dumps({
            "orderId": order["order_id"],
            "userId": order["user_id"],
            "newStatus": order["status"]
        })
    )
    response = Response(status_code=status.HTTP_200_OK)
    return response
