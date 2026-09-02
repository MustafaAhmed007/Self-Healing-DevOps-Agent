.PHONY: install test lint typecheck demo eval api
install:
	python -m pip install -e '.[dev]'
test:
	pytest -q
lint:
	ruff check .
typecheck:
	mypy app
demo:
	python -m app.cli demo
eval:
	python -m evals.harness
api:
	uvicorn app.api:app --reload
