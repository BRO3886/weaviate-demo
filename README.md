# Image Search App

## Setup

### Run Weaviate

```bash
make run-weaviate
```

This will start Weaviate in the background on port 8080. You can check the logs with:

```bash
make check-weaviate-logs
```

### Download Flickr30k dataset (NOT REQUIRED FOR NOW)

> Update: The dataset is now downloaded automatically See `app/data/images.py`.

Install [git-lfs](https://git-lfs.github.com/)

After installing git-lfs, enable it:

```bash
git lfs install
git clone https://huggingface.co/datasets/lmms-lab/flickr30k
```

### Install dependencies

This will create a virtual environment and install the dependencies via uv. To install uv, see the [uv docs](https://docs.astral.sh/uv/getting-started/installation/).

```bash
make install
```

### Run Indexer

```bash
make run-indexer
```

To modify the number of images to index, change the `count` variable in the Makefile.

```Makefile
count := 100
install:
    uv venv
    ...
```

This will start the indexer module. The logs will be printed to the console.

### Run the API

```bash
make build-api-docker
```

This will build the API docker image.

```bash
make up
```

This will start the FastAPI docker container on port 8000. To check the logs, run:

```bash
make check-api-logs
```

To verify the API is running, you can make a request to the `/health` endpoint:

```bash
curl http://localhost:8000/health
```

This should return a 200 status code. The API docs are available at:

```
http://localhost:8000/docs
```

## Run the frontend

```bash
make run-frontend
```

This will start the frontend on port 5173.

![Screnshot of the frontend](https://i.ibb.co/DDn6jQ75/image.png)
