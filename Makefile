install:
	pip install -e .

test:
	pytest

lint:
	ruff check .
	black .

coverage:
	pytest --cov=gitter --cov-report=term-missing
