from fastapi import APIRouter, Depends

from app.core import get_embedder
from app.core.embedder import Embedder

health_router = APIRouter()


@health_router.get("/health")
async def health(embedder: Embedder = Depends(get_embedder)):
    return {"status": "ok", "model": embedder.model._get_name()}
