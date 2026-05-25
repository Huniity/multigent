.PHONY: help up up-dev up-prod clean migrate-dev migrate-prod migration-dev migration-prod superuser-dev superuser-prod check-dev check-prod backend-test-dev backend-test-prod frontend-test test

requirements: ## Generate requirements.txt from pyproject.toml
	uv pip compile ./srcs/backend/pyproject.toml -o ./srcs/backend/requirements.txt

prepare: ## Prepare the development environment by creating a virtual environment, installing Python 3.12, and syncing dependencies
	rm -rf .venv
	uv python install 3.12
	uv python pin 3.12
	uv sync
	uv run crewai

check: ## Check for any issues in the codebase using ruff
	uv run ruff check

format: ## Format the codebase using ruff
	uv run ruff format

fullCheck: check format

pre-commit-all: ## Run pre-commit checks on all files
	uv run pre-commit run --all-files

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

env: ## Create .env file if it doesn't exist
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		printf "POSTGRES_DB=multi_db\n" > .env; \
		printf "POSTGRES_USER=multi_dev\n" >> .env; \
		printf "POSTGRES_PASSWORD=multi_2026\n" >> .env; \
		printf "DATABASE_URL=postgres://multi_dev:multi_2026@db:5432/multi_db\n" >> .env; \
		printf "DEBUG=True\n" >> .env; \
		printf "ALLOWED_HOSTS=localhost,127.0.0.1,backend, *\n" >> .env; \
		printf "DJANGO_SETTINGS_MODULE=core.settings\n" >> .env; \
		printf "SECRET_KEY=django-insecure-n@yjki0(^_d89!g@0u8t77ao-q&=l#m!^-98kaz@#*hud5j62*\n" >> .env; \
		printf "GEMINI_API_KEY=\n" >> .env; \
		printf "MODEL=gemini-2.5-flash\n" >> .env; \
		printf "\n" >> .env; \
		printf "# Production settings\n" >> .env; \
		printf "\n" >> .env; \
		printf "# ALLOWED_HOSTS=ootb.com,www.ootb.com\n" >> .env; \
		printf "# DEBUG=False\n" >> .env; \
	else \
		echo ".env file already exists."; \
	fi
	@echo "Environment variables:"
	@cat .env



start-dev: ## Start dev workflow with strict database readiness check
	@echo "Starting Docker containers in background..."
	docker compose -f compose.yaml up --build -d
	@echo "Waiting for PostgreSQL and Django backend to be fully ready..."
	@until docker compose -f compose.yaml exec backend python manage.py check > /dev/null 2>&1; do \
		echo "Backend not ready yet... checking again in 2 seconds"; \
		sleep 2; \
	done
	@echo "Backend is ready! Running migrations and setup..."
	$(MAKE) migration-dev
	$(MAKE) migrate-dev
	$(MAKE) superuser-dev
	@echo "Setup complete! Attaching to container logs..."
	docker compose -f compose.yaml logs -f

sync-dev:
	cd srcs/frontend && npm install && cd ../../ && cd srcs/backend && uv sync && cd ../../

up: ## Start production environment on port 80 (alias for up-prod)
	docker compose -f compose.prod.yaml up --build

up-dev: ## Start development environment
	docker compose -f compose.yaml up
	$(MAKE) migrate-dev

up-prod: ## Start production environment
	docker compose -f compose.prod.yaml up --build

clean: ## Stop and remove all containers, volumes, and orphans
	docker compose -f compose.yaml down -v --remove-orphans
	docker compose -f compose.prod.yaml down -v --remove-orphans

migrate-dev: ## Run database migrations in development environment
	docker compose -f compose.yaml exec backend python manage.py migrate

migrate-prod: ## Run database migrations in production environment
	docker compose -f compose.prod.yaml exec backend python manage.py migrate

migration-dev: ## Create new database migrations in development environment
	docker compose -f compose.yaml exec backend python manage.py makemigrations

migration-prod: ## Create new database migrations in production environment
	docker compose -f compose.prod.yaml exec backend python manage.py makemigrations

superuser-dev: ## Create a superuser in development environment
	docker compose -f compose.yaml exec backend python manage.py createsuperuser

superuser-prod: ## Create a superuser in production environment
	docker compose -f compose.prod.yaml exec backend python manage.py createsuperuser

check-dev: ## Check for any issues in development environment
	docker compose -f compose.yaml exec backend python manage.py check

check-prod: ## Check for any issues in production environment
	docker compose -f compose.prod.yaml exec backend python manage.py check

backend-test-dev: ## Run backend tests in development environment
	docker compose -f compose.yaml exec backend uv run pytest

backend-test-prod: ## Run backend tests in production environment
	docker compose -f compose.prod.yaml exec backend uv run pytest

frontend-test: ## Run frontend tests
	cd srcs/frontend && npm run test

test: ## Run backend and frontend test suites sequentially
	$(MAKE) backend-test-dev
	$(MAKE) frontend-test

logs-backend-dev: ## Backend logs in development environment
	docker compose -f compose.yaml exec backend tail -f /app/logs/django.log

logs-backend-prod: ## Backend logs in production environment
	docker compose -f compose.prod.yaml exec backend tail -f /app/logs/django.log

logs-pytest-dev: ## Pytest logs in development environment
	docker compose -f compose.yaml exec backend cat /app/logs/pytest.log

logs-pytest-prod: ## Pytest logs in production environment
	docker compose -f compose.prod.yaml exec backend cat /app/logs/pytest.log
