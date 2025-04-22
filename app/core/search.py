from abc import ABC, abstractmethod

from PIL import Image
from weaviate import WeaviateAsyncClient, WeaviateClient

from app.data.collection import ImageCaption


class Search(ABC):
    @abstractmethod
    def index(self, data: Image.Image | str):
        pass

    @abstractmethod
    def search(self, query):
        pass


class WeaviateSearch(Search):
    def __init__(self, client: WeaviateClient):
        self.client = client

    def create_collections_if_not_exists(self):
        if not self.client.collections.exists("ImageCaption"):
            self.client.collections.create_from_dict(ImageCaption)

    def index(self, data):
        pass

    def search(self, query):
        pass
