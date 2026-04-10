# n8n-workflow-tools Makefile
.PHONY: install dev test lint build publish docker clean

install:
	pip install .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/
	mypy src/

build:
	python -m build

publish: build
	twine upload dist/*

docker:
	docker build -t n8n-workflow-tools .

clean:
	rm -rf dist/ build/ *.egg-info src/*.egg-info __pycache__ .mypy_cache .ruff_cache
