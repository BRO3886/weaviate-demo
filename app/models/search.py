from typing import List

from pydantic import BaseModel

from app.services.search import Document


class TextSearchRequest(BaseModel):
    query: str
    top_k: int = 10


class SearchResponse(BaseModel):
    results: List[Document]
