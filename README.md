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

Using Docker via Makefile:

```bash
make docker-test
```

## Wishlist (time constraints)

Stuff I would have added with more time:

- Async support from the start
- OpenAPI support (expanded docs/spec)
- Separate repos for FE and BE
