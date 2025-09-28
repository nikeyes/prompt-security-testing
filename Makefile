.PHONY: default
default: lint

.PHONY: lint
lint:
	uv run ruff check
	uv run yamllint .

.PHONY: lint-fix
lint-fix:
	uv run ruff format
	uv run ruff check --fix-only 
	uv run ruff check

.PHONY: install
install:
	uv sync

.PHONY: test
test:
	uv run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing tests/

.PHONY: run
run:
	uv run python src/main.py $(USE_CASE)


# .PHONY: ci-tests
# ci-tests:
# 	poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing tests/ -m "not real_provider"