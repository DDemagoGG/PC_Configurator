import json
from datetime import datetime, timedelta

from fastapi import *
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from schemas.order import CreateOrderForm, Order, NearlyOrder
from services.auth import get_user_id_from_token, validate_access_token_for_user
from services.order import create_order, get_parameters

from repository.redis import redis_client

router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.post("/user/saveorder")
async def save_user_order(order: NearlyOrder, request: Request):
    print(order.model_dump_json())
    user_id = get_user_id_from_token(request)
    redis_client.set(f"user_order_draft:{user_id}", order.model_dump_json(), ex=3600 * 30)
    return Response(status_code=status.HTTP_200_OK)


@router.get("/user/order", response_class=responses.HTMLResponse)
async def show_cretion_order_page(request: Request):
    if validate_access_token_for_user(request):
        user_id = get_user_id_from_token(request)
        token = request.cookies.get("access_token")
        redis_token = redis_client.get(f"auth_user_token:{user_id}")
        if redis_token == token:
            params = {"request": request}
            params["shops"] = await get_parameters()
            return template.TemplateResponse("Order.html", params)
    return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)


@router.post("/user/order")
async def create_order_handle(request: Request, order: CreateOrderForm):
    user_id = get_user_id_from_token(request)
    await create_order(order.order.model_dump(), order.shop_id, user_id)
    if redis_client.exists(f"user_order_draft:{user_id}") == 1:
        redis_client.delete(f"user_order_draft:{user_id}")
    response = Response(status_code=status.HTTP_200_OK)
    return response
