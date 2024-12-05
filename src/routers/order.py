import json
from datetime import datetime, timedelta

from fastapi import *
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from schemas.order import CreateOrderForm
from services.auth import get_user_id_from_token, validate_access_token_for_user
from services.order import create_order, get_parameters

router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.get("/user/order", response_class=responses.HTMLResponse)
async def show_cretion_order_page(request: Request):
    if validate_access_token_for_user(request):
        params = {"request": request}
        params["shops"] = await get_parameters()
        return template.TemplateResponse("Order.html", params)
    return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)


@router.post("/user/order")
async def create_order_handle(request: Request, order: CreateOrderForm):
    user_id = get_user_id_from_token(request)
    await create_order(order.order.model_dump(), order.shop_id, user_id)
    response = Response(status_code=status.HTTP_200_OK)
    return response
