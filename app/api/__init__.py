from fastapi import APIRouter

from app.api.routes.health import health_router

router = APIRouter()
router.include_router(health_router)
