from app.core.embedder import Embedder

_embedder = Embedder()


def get_embedder() -> Embedder:
    return _embedder
