.PHONY: docker-up docker-down run-consumer run-producer run-app

docker-up:
	docker compose up

docker-down:
	docker compose down

run-consumer:
	python historical_price_consumer.py

run-producer:
	python historical_price_producer.py

run-list-company:
	python run_crawl_listing_company.py

run-app:
	start cmd /k make run-consumer && start cmd /k make run-producer

spark-submit:
	start cmd /k make run-producer && start cmd /k docker run spark_kafka_consumer
