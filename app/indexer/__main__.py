import argparse
import concurrent.futures
import io
import logging
from typing import Any, Dict, List

import weaviate
from datasets import Dataset
from PIL import Image

from app.config import get_config
from app.core.logger import get_logger
from app.data.images import image_dataset
from app.services import get_embedder
from app.services.embedder import Embedder
from app.services.search import IndexableDoc, WeaviateSearch

BATCH_SIZE = get_config().get("indexer.batch_size", 100)
MAX_COUNT = 31783


def index_batch(
    batch_index: int,
    batch: Dataset,
    search: WeaviateSearch,
    logger: logging.Logger,
):
    logger.info("indexing batch %d", batch_index)
    image_data_list: List[Dict] = batch["image"]
    captions_list: List[List[str]] = batch["caption"]
    img_ids: List[str] = batch["img_id"]
    filenames: List[str] = batch["filename"]
    sent_ids_list: List[List[str]] = batch["sentids"]
    num_items = len(image_data_list)
    if num_items == 0:
        logger.info(f"Batch {batch_index} is empty, skipping.")
        return

    for i in range(num_items):
        img_data = image_data_list[i]
        filename = filenames[i]
        img_id = img_ids[i]
        sent_ids = sent_ids_list[i]
        captions = captions_list[i]

        current_image = Image.open(io.BytesIO(img_data["bytes"]))
        index_row(
            {
                "image": current_image,
                "caption": captions,
                "img_id": img_id,
                "filename": filename,
                "sentids": sent_ids,
            },
            search,
            logger,
        )


def index_row(
    row: Dict[str, Any],
    search: WeaviateSearch,
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
        search.index(IndexableDoc(img_id, image, captions, path))
    except Exception as e:
        logger.error("error embedding image %s: error: %s", img_id, e)

    logger.info("indexed image %s", img_id)


def index(logger: logging.Logger, dataset: Dataset):
    config = get_config()
    logger.info("Indexing dataset")
    # ['image', 'caption', 'sentids', 'img_id', 'filename']
    # logger.debug("dataset columns: %s", image_dataset.column_names)
    batched_dataset = dataset.batch(BATCH_SIZE)
    logger.info("batching complete: created %d batches", len(batched_dataset))

    client = weaviate.connect_to_local(
        host=config.get("weaviate.host", "localhost"),
        port=config.get("weaviate.port", 8080),
    )
    embedder = get_embedder()

    try:
        search = WeaviateSearch(client, embedder)
        search.create_collections_if_not_exists()

        # for row in image_dataset:
        #     index_row(row, search, embedder, logger)
        # logger.info("all rows indexed")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i, batch in enumerate(batched_dataset):
                logger.info("indexing batch %d of %d", i, len(batched_dataset))
                futures.append(executor.submit(index_batch, i, batch, search, logger))

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error("Error processing batch: %s", e)
        logger.info("all batches indexed")

    except Exception as e:
        logger.error("Error indexing dataset: %s", e)
    finally:
        client.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Index images and captions")
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Number of images to index (default: all)",
    )
    args = parser.parse_args()
    logger = get_logger("indexer")
    if args.count is not None:
        if args.count > MAX_COUNT:
            logger.warning(
                "count is greater than the maximum number of images to index, setting count to %d",
                MAX_COUNT,
            )
            args.count = MAX_COUNT

        dataset = image_dataset.select(range(args.count))
        index(logger, dataset)
    else:
        index(logger, image_dataset)
