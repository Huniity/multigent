prepare:
	rm -rf .venv
	uv python install 3.12
	uv python pin 3.12
	uv sync
	uv run crewai