import json
from datetime import datetime, timedelta

from fastapi import *
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from services.auth import get_user_id_from_token, validate_access_token_for_user
from services.personal import get_parameters

router = APIRouter()

template = Jinja2Templates(directory="templates")


@router.get("/user/account", response_class=responses.HTMLResponse)
async def show_login_page(request: Request):
    if validate_access_token_for_user(request):
        user_id = get_user_id_from_token(request)
        parameters = await get_parameters(user_id)
        parameters["request"] = request
        return template.TemplateResponse("PersonalAccount.html", parameters)

    return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)
