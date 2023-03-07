install:
	poetry install

tests:
	poetry run pytest -vv tests

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

lint:
	poetry run flake8 .

dev:
	poetry run flask --app page_analyzer:app run

.PHONY: tests