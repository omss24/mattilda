# Mattilda Backend Challenge API

## Run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000.

## Run migrations (Alembic)

```bash
poetry run alembic upgrade head
```

## Run tests

Using Poetry locally:

```bash
poetry install
poetry run pytest
```
