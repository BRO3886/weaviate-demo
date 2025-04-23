import logging
import time

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.models.search import TextSearchRequest
from app.services import get_weaviate
from app.services.search import WeaviateSearch

search_router = APIRouter()


@search_router.post("/search-text")
async def search_text(
    body: TextSearchRequest,
    weaviate: WeaviateSearch = Depends(get_weaviate),
    logger: logging.Logger = Depends(get_logger),
):
    start_time = time.time()
    query = body.query.strip()
    if not query:
        return JSONResponse(content={"error": "query is required"}, status_code=400)

    top_k = body.top_k
    if top_k < 1:
        return JSONResponse(
            content={"error": "top_k must be greater than 0"}, status_code=400
        )

    try:
        results = weaviate.search(query, top_k)
        end_time = time.time()
        logger.debug(f"time taken to search: {end_time - start_time} seconds")
        return JSONResponse(
            content={
                "results": results,
                "query_time": (end_time - start_time) * 1000,
            }
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
