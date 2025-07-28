FROM python:3.11.7-slim AS builder

ENV HTTP_PROXY=    

ENV HTTPS_PROXY=    

ENV http_proxy=  

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN python -m venv /app/venv

RUN . /app/venv/bin/activate && \
    pip install --upgrade pip setuptools && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main

FROM python:3.11.7-slim

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/venv/bin:$PATH"

CMD [ "python","main.py","--env","prod" ]