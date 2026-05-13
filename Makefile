prepare:
	rm -rf .venv
	uv python install 3.12
	uv python pin 3.12
	uv sync
	uv run crewai

check:
    uv run ruff check

format:
    uv run ruff format

fullCheck: check format

pre-commit-all:
	uv run pre-commit run --all-files
