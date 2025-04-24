
count := 100

install:
	uv venv
	uv sync
	cd frontend && npm install

up:
	docker compose up -d

down:
	docker compose down

check-app:
	docker logs -f image-search-app-1

run-app:
	uvicorn app.main:app

run-dev:
	uvicorn app.main:app --reload

run-indexer:
	uv run -m app.indexer --count $(count)

build-api-docker:
	docker compose build

run-weaviate:
	docker compose up -d weaviate

stop-weaviate:
	docker compose stop weaviate

check-weaviate-logs:
	docker logs -f image-search-weaviate-1

check-api-logs:
	docker logs -f image-search-app-1

run-frontend:
	cd frontend && npm run dev