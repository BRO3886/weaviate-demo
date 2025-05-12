from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TextSearchRequest(BaseModel):
    query: str
    top_k: int = 10


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]


class AdditionalWeaviateParams(BaseModel):
    tags: Optional[List[str]] = None
