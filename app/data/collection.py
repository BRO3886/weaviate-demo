Image = {
    "class": "Image",
    "description": "Stores image URL and its precomputed vector.",
    "vectorizer": "none",
    "vectorIndexType": "hnsw",
    "vectorIndexConfig": {"distance": "cosine"},
    "properties": [
        {
            "name": "imageUrl",
            "dataType": ["text"],
            "description": "The URL where the image is hosted.",
            "indexFilterable": True,
            "indexSearchable": False,
        }
    ],
}


Caption = {
    "class": "Caption",
    "description": "Stores individual caption text, its precomputed vector, and a link to the parent image.",
    "vectorizer": "none",
    "vectorIndexType": "hnsw",
    "vectorIndexConfig": {"distance": "cosine"},
    "properties": [
        {
            "name": "captionText",
            "dataType": ["text"],
            "description": "The text content of the caption.",
            "indexFilterable": True,
            "indexSearchable": True,
            "tokenization": "word",
        },
        {
            "name": "forImage",
            "dataType": ["Image"],
            "description": "The image this caption describes.",
        },
    ],
}
