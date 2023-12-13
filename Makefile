.PHONY: init run-consumer run-producer run-list-company run-app

init:
	python FolderMaker.py

run-consumer:
	python historical_price_consumer.py

run-producer:
	python historical_price_producer.py

run-list-company:
	python run_crawl_listing_companies.py

run-app:
	start cmd /k make run-consumer && start cmd /k make run-producer