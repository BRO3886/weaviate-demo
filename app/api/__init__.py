from fastapi import APIRouter

from app.api.routes.health import health_router
from app.api.routes.search import search_router

router = APIRouter()
router.include_router(health_router)
router.include_router(search_router)
