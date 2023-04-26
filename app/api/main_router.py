from fastapi import APIRouter
from app.core.config import settings
from datetime import datetime

from app.api.auth import router as auth_router
from app.api.post import router as post_router

router = APIRouter(prefix=settings.API_V1_STR)


@router.get("/")
def get_home():
    return {"server_time": datetime.now()}


# @router.get()
router.include_router(auth_router)
router.include_router(post_router)
