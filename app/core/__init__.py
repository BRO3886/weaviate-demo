import weaviate

from app.core.embedder import Embedder
from app.core.search import WeaviateSearch

_embedder: Embedder | None = None
_client: weaviate.WeaviateClient = None
_search: WeaviateSearch | None = None


def get_weaviate() -> WeaviateSearch:
    return _search


def get_embedder() -> Embedder:
    return _embedder


async def init_services():
    global _embedder, _client, _search
    _embedder = Embedder()
    _client = weaviate.connect_to_local()
    _search = WeaviateSearch(client=_client)
    _search.create_collections_if_not_exists()


async def close_services():
    global _embedder, _client, _search
    if _embedder is not None:
        _embedder.__exit__(None, None, None)

    if _client is not None:
        _client.close()
