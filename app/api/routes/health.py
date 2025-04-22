import logging

from fastapi import APIRouter, Depends

from app.core import get_embedder
from app.core.embedder import Embedder
from app.core.logger import get_logger

health_router = APIRouter()


@health_router.get("/health")
async def health(
    embedder: Embedder = Depends(get_embedder),
    logger: logging.Logger = Depends(get_logger),
):
    logger.info("Health check")
    return {"status": "ok", "model": embedder.model._get_name()}
