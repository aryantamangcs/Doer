FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv
RUN uv pip install --system .

COPY . .

EXPOSE 8080

CMD ["uvicorn","src.main:app","--host","0.0.0.0","--reload","--port","8080"]


