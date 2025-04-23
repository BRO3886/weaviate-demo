import json
from abc import ABC, abstractmethod
from typing import List, Tuple
from uuid import UUID

from PIL import Image
from weaviate import WeaviateAsyncClient, WeaviateClient, collections
from weaviate.collections.classes.data import DataReference

from app.core.embedder import Embedder
from app.core.logger import get_logger
from app.data.collection import Caption as CaptionCollection
from app.data.collection import Image as ImageCollection


class Document:
    def __init__(
        self, id: str, image: Image.Image, captions: List[str], image_url: str
    ):
        self._id = id
        self._image = image
        self._captions = captions
        self._image_url = image_url

    @property
    def id(self) -> str:
        return self._id

    @property
    def image(self) -> Image.Image:
        return self._image

    @property
    def captions(self) -> List[str]:
        return self._captions

    @property
    def image_url(self) -> str:
        return self._image_url

    def __str__(self) -> str:
        return self.id


class Search(ABC):
    @abstractmethod
    def index(self, data: Tuple[Image.Image, List[str]]):
        pass

    @abstractmethod
    def search(self, query):
        pass


class WeaviateSearch(Search):
    def __init__(self, client: WeaviateClient, embedder: Embedder):
        self.client = client
        self.embedder = embedder
        self.logger = get_logger("weaviate_search")

    def create_collections_if_not_exists(self):
        if not self.client.collections.exists("Image"):
            self.client.collections.create_from_dict(ImageCollection)
        if not self.client.collections.exists("Caption"):
            self.client.collections.create_from_dict(CaptionCollection)

    def generate_embeddings(self, document: Document):
        self.logger.debug(f"generating embeddings for document: {document}")
        image_embedding = self.embedder.embed_image(document.image)
        text_embeddings = [
            self.embedder.embed_text(caption) for caption in document.captions
        ]
        return image_embedding, text_embeddings

    def index(self, document: Document):
        self.logger.debug(f"indexing document: {document}")
        image_embedding, text_embeddings = self.generate_embeddings(document)
        image_collection = self.client.collections.get("Image")
        img_uuid = image_collection.data.insert(
            properties={
                "imageUrl": document.image_url,
            },
            vector=image_embedding,
        )
        caption_collection = self.client.collections.get("Caption")
        caption_uuids: List[UUID] = []
        for i, caption in enumerate(document.captions):
            caption_uuid = caption_collection.data.insert(
                properties={
                    "captionText": caption,
                },
                vector=text_embeddings[i],
            )
            caption_uuids.append(caption_uuid)
        caption_collection.data.reference_add_many(
            [
                DataReference(
                    from_property="forImage",
                    from_uuid=caption_uuid,
                    to_uuid=img_uuid,
                )
                for caption_uuid in caption_uuids
            ]
        )

    def search(self, query):
        pass
