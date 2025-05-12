import os
from os import path

from datasets import Dataset, load_dataset

from app.core.logger import get_logger

logger = get_logger(__name__)

# data_files = [
#     "test-00000-of-00009.parquet",
#     "test-00001-of-00009.parquet",
#     "test-00002-of-00009.parquet",
#     "test-00003-of-00009.parquet",
#     "test-00004-of-00009.parquet",
#     "test-00005-of-00009.parquet",
#     "test-00006-of-00009.parquet",
#     "test-00007-of-00009.parquet",
#     "test-00008-of-00009.parquet",
# ]
# logger.info("loading dataset")
# image_dataset: Dataset = load_dataset(
#     "parquet",
#     data_files=[path.join("flickr30k/data", f) for f in data_files],
#     split="train",
# )
# logger.info("dataset loaded with %d rows", image_dataset.num_rows)


image_dataset = load_dataset("lmms-lab/flickr30k")


# def get_image_dataset_dict() -> dict:
#     image_dataset = {
#         "image": [],
#         "caption": [],
#         "img_id": [],
#         "filename": [],
#         "sentids": [],
#     }
#     for file in os.listdir("images"):
#         logger.info("processing image: %s", file)
#         with open(path.join("images", file), "rb") as f:
#             image_bytes = f.read()
#             image_dataset["image"].append({"bytes": image_bytes})
#             caption = file.split("-")[0]
#             image_dataset["caption"].append([caption])
#             image_dataset["img_id"].append(file)
#             image_dataset["filename"].append(file)
#             image_dataset["sentids"].append([file])
#     logger.info("dataset created with %d rows", len(image_dataset["image"]))
#     return image_dataset


# image_dataset: Dataset = Dataset.from_dict(get_image_dataset_dict())
