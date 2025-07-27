FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY reqs.txt .
COPY src/ ./src/

RUN pip install --no-cache-dir -r reqs.txt

CMD ["python3", "-m", "src.controllers.event"]
