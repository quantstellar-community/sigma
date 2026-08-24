.PHONY: sync test lint format format-fix type check run

sync:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format --check .

format-fix:
	uv run ruff format .

type:
	uv run pyright

check: lint format type test

run:
	uv run uvicorn sigma.api.main:app --reload
