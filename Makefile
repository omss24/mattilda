build:
	docker-compose build

up:
	docker-compose up

up-build:
	docker-compose up --build

test:
	poetry run pytest

docker-up-build:
	docker-compose up --build -d

docker-test: docker-up-build
	docker-compose run --rm api poetry run pytest

docker-down:
	docker-compose down

.PHONY: build up up-build test docker-up-build docker-test docker-down
