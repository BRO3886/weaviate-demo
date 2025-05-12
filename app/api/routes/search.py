import logging
import time
from http.client import HTTPException

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

from app.core.llm import llm
from app.core.logger import get_logger
from app.models.exceptions import InternalServerError, ValidationError
from app.models.search import AdditionalWeaviateParams, TextSearchRequest
from app.services import get_weaviate
from app.services.search import WeaviateSearch

search_router = APIRouter()


knowldege_graph = {
    # exhaustive list of tags for the search space
    # query -> extract tags (what tags are there in the query)
    # while searching in weaviate, use the tags to filter the results
}


@search_router.post("/search-text")
async def search_text(
    body: TextSearchRequest,
    weaviate: WeaviateSearch = Depends(get_weaviate),
    logger: logging.Logger = Depends(get_logger),
):
    start_time = time.time()
    query = body.query.strip()
    if not query:
        raise ValidationError(message="query is required")

    top_k = body.top_k
    if top_k < 1:
        raise ValidationError(message="top_k must be greater than 0")

    try:
        tags = llm.generate_tags(query)
        results = weaviate.search(
            query, top_k, additional_params=AdditionalWeaviateParams(tags=tags)
        )
        end_time = time.time()
        logger.debug(f"time taken to search: {end_time - start_time} seconds")
        return JSONResponse(
            content={
                "results": results,
                "query_time": (end_time - start_time) * 1000,
            }
        )
    except Exception as e:
        raise InternalServerError(message=str(e))


@search_router.post("/search-image")
async def search_image(
    file: UploadFile = File(...),
    weaviate: WeaviateSearch = Depends(get_weaviate),
    logger: logging.Logger = Depends(get_logger),
):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise ValidationError(message="file must be an image")

    image = Image.open(file.file)
    try:
        results = weaviate.image_search(image)
        return JSONResponse(content={"results": results}, status_code=200)
    except Exception as e:
        raise InternalServerError(message=str(e))
