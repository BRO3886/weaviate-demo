from os import path

from datasets import load_dataset

data_files = [
    "test-00000-of-00009.parquet",
    "test-00001-of-00009.parquet",
    "test-00002-of-00009.parquet",
    "test-00003-of-00009.parquet",
    "test-00004-of-00009.parquet",
    "test-00005-of-00009.parquet",
    "test-00006-of-00009.parquet",
    "test-00007-of-00009.parquet",
    "test-00008-of-00009.parquet",
]
image_dataset = load_dataset(
    "parquet",
    data_files=[
        path.join("/Users/sidv/Desktop/projects/go/typeface/flickr30k/data", f)
        for f in data_files
    ],
)
