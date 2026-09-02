PYTHON ?= python

.PHONY: install test lint typecheck run-api demo doctor eval docker-up docker-down

install:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest

lint:
	ruff check .

typecheck:
	mypy app packages

run-api:
	uvicorn app.api:app --reload

demo:
	$(PYTHON) -m app.cli demo

doctor:
	$(PYTHON) -m app.cli doctor

eval:
	$(PYTHON) -m evals.harness

docker-up:
	docker compose up -d

docker-down:
	docker compose down
