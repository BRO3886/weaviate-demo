import concurrent.futures
import logging
from collections import deque
from typing import Any, Dict, List

import weaviate
from datasets import IterableDataset
from PIL import Image

from app.core import get_embedder
from app.core.embedder import Embedder
from app.core.logger import get_logger
from app.core.search import Document, WeaviateSearch
from app.data.images import image_dataset

BATCH_SIZE = 100


def index_batch(
    batch_index: int,
    batch: Dict[str, List[Any]],
    search: WeaviateSearch,
    embedder: Embedder,
    logger: logging.Logger,
):
    logger.info("indexing batch %d", batch_index)
    # {
    #     "image": ["list of image objects"],
    #     "caption": ["list of captions"],
    #     "sentids": ["list of sentence ids"],
    #     "img_id": ["list of image ids"],
    #     "filename": ["list of image filenames"],
    # }

    n = len(batch.get("image"))
    logger.info("indexing %d images", n)
    i = 0
    for i in range(n):
        try:

            images = batch.get("image")
            captions = batch.get("caption")
            sentids = batch.get("sentids")
            img_ids = batch.get("img_id")
            filenames = batch.get("filename")
        except Exception as e:
            logger.error("error getting batch: %s", e)
            break

        # if (
        #     images is None
        #     or captions is None
        #     or sentids is None
        #     or img_ids is None
        #     or filenames is None
        # ):
        #     break

        image = images.pop()
        curr_img = Image.frombytes(data=image["bytes"])
        logger.info("image: %s", type(curr_img))
        curr_captions: List[str] = captions.pop()
        curr_sentids: List[str] = sentids.pop()
        curr_img_id: str = img_ids.pop()
        curr_filename: str = filenames.pop()
        print(curr_filename)

        try:
            # search.index(Document(curr_img, curr_captions))
            pass
        except Exception as e:
            logger.error(
                "error embedding image %s: error: %s curr: %d",
                curr_img_id,
                e,
                i,
            )


def index_row(
    row: Dict[str, Any],
    search: WeaviateSearch,
    embedder: Embedder,
    logger: logging.Logger,
):
    image: Image.Image = row["image"]
    captions = row["caption"]
    sentids = row["sentids"]
    img_id = row["img_id"]
    filename = row["filename"]
    try:
        path = f"static/{filename}"
        image.save(path)
        search.index(Document(img_id, image, captions, path))
    except Exception as e:
        logger.error("error embedding image %s: error: %s", img_id, e)

    logger.info("indexed image %s", img_id)


def index(logger: logging.Logger):
    logger.info("Indexing dataset")
    # ['image', 'caption', 'sentids', 'img_id', 'filename']
    logger.debug("dataset columns: %s", image_dataset.column_names)
    # batched_dataset = image_dataset.batch(BATCH_SIZE)
    # logger.info("batching complete: created %d batches", len(batched_dataset))

    client = weaviate.connect_to_local()
    embedder = get_embedder()

    try:
        search = WeaviateSearch(client, embedder)
        search.create_collections_if_not_exists()

        i = 0
        for row in image_dataset:
            i += 1
            index_row(row, search, embedder, logger)
            if i == 5:
                break
        logger.info("all rows indexed")

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     futures = []
        #     for i, batch in enumerate(batched_dataset):
        #         logger.info("indexing batch %d of %d", i, len(batched_dataset))
        #         futures.append(
        #             executor.submit(index_batch, i, batch, search, embedder, logger)
        #         )
        #     concurrent.futures.wait(futures)
        # logger.info("all batches indexed")

    except Exception as e:
        logger.error("Error indexing dataset: %s", e)
    finally:
        client.close()


if __name__ == "__main__":
    import warnings

    warnings.filterwarnings("ignore", category=ResourceWarning)
    logger = get_logger("indexer")
    index(logger)
