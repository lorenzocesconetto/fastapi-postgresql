from fastapi import APIRouter

from app.api.api_v1 import items, login, users, utils
from app.core.config import settings

api_v1_router = APIRouter(prefix=settings.API_V1_STR)
api_v1_router.include_router(login.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(utils.router)
api_v1_router.include_router(items.router)
