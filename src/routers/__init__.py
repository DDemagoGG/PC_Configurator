from fastapi import *
from starlette.templating import Jinja2Templates

from routers.auth import router as auth_router
from routers.home import router as home_router
from routers.order import router as order_router
from routers.personal import router as personal_router
from routers.shophome import router as shop_router
from schemas.user import LoginUserForm

router = APIRouter()

router.include_router(auth_router)
router.include_router(home_router)
router.include_router(personal_router)
router.include_router(shop_router)
router.include_router(order_router)
