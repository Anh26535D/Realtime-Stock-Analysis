FROM python:3.9.5-slim-buster

WORKDIR /app

COPY crawler/ ./crawler
COPY utils/ ./utils
COPY data/ ./data
COPY producers/ ./producers
COPY requirements.txt .
COPY logs/ ./logs

RUN apt-get update \
    && apt-get install nano \
    && apt-get -y install libpq-dev gcc \
    && python3 -m pip install -r requirements.txt

CMD ["python3", "producers/historical_price_producer.py"]
