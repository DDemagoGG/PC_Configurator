from asyncpg import create_pool
from fastapi import *
from starlette.staticfiles import *

from routers import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(router)
