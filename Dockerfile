FROM python:3.11-slim

WORKDIR /app

ENV POETRY_VERSION=1.8.2
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml /app/pyproject.toml
RUN poetry config virtualenvs.create false \
	&& poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
