set shell := ["powershell.exe", "-c"]

# Run the test suite (pytest and behave)
test:
    uv run pytest --cov=vindicta_foundation -n auto
    uv run behave

# Run linters, format checkers, and type checkers
lint:
    uv run ruff format --check .
    uv run ruff check .
    uv run mypy src tests

# Serve the documentation locally
docs:
    $env:NO_MKDOCS_2_WARNING="1"; uv run mkdocs serve

# Sync current environment
sync:
    uv sync --all-extras

# Run validation before pushing to catch regressions
prepush: lint test
    @echo "Pre-push checks passed successfully!"
