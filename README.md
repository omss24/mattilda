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
- Invoice status transition state machine (enforce pending → partially_paid → paid)
- JWT/OAuth2 authentication instead of shared API key
- Rate limiting middleware
- Cursor-based pagination for large datasets
- PostgreSQL in tests (testcontainers) instead of SQLite
- Concurrency handling for payments (SELECT FOR UPDATE)
- Multi-stage Docker build with non-root user
- Database CHECK constraints on amounts and dates
- Request ID tracking for distributed logging
- Comprehensive API documentation with examples
