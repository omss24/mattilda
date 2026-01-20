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

## AWS Infrastructure (Terraform)

> ⚠️ **DISCLAIMER**: The Terraform configuration has **NOT been tested on a real AWS account**. It is provided as a reference implementation demonstrating infrastructure-as-code best practices.

The `terraform/` directory contains IaC for deploying to AWS:

- **VPC** with public subnets across 2 AZs
- **ECS Fargate** for running the containerized backend
- **Application Load Balancer** for traffic distribution
- **RDS PostgreSQL** for the database
- **ElastiCache Redis** for caching (optional)
- **CloudWatch Logs** for container logging

### Quick Start

```bash
cd terraform

# Initialize
terraform init

# Create terraform.tfvars with your values
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your backend_image, db_password, api_key

# Review changes
terraform plan

# Deploy
terraform apply

# Get the API URL
terraform output api_url
```

See [terraform/README.md](terraform/README.md) for full documentation.

## Wishlist (time constraints)

Stuff I would have added with more time:

- Async support from the start
- OpenAPI support (expanded docs/spec)
- Vue frontend for demoing the API
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

