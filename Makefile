up:
	docker compose up -d

down:
	docker compose down

check-weaviate:
	docker logs -f image-search-weaviate-1
