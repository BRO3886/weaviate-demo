import weaviate

from app.core.search import WeaviateSearch
from app.data.images import image_dataset

if __name__ == "__main__":
    with weaviate.connect_to_local() as client:
        search = WeaviateSearch(client)
        search.index(image_dataset)
        client.close()
