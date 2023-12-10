.PHONY: build-producer restart run-listing

build-producer:
	docker build -t stock-producer .

restart:
	docker-compose down && docker-compose --env-file .\.env up -d --remove-orphans --build && docker ps

run-listing:
	python run_crawl_listing_companies.py

