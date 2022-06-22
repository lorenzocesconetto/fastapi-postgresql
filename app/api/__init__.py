from app.api.api_v1 import api_v1_router
from fastapi import APIRouter
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_STR)
api_router.include_router(api_v1_router)
