up:
	docker compose up -d

down:
	docker compose down

check-weaviate:
	docker logs -f image-search-weaviate-1

run-app:
	uvicorn app.main:app

run-dev:
	uvicorn app.main:app --reload
