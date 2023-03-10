install-poetry:
	pip install poetry

install:
	poetry install

init-db:
	psql $(DATABASE_URL) < database.sql

build: install-poetry install init-db

tests:
	poetry run pytest -vv tests

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

lint:
	poetry run flake8 .

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

.PHONY: tests