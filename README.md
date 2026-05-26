# Multigent

> A multi-agent AI council that reviews your code so you don't have to guess what's wrong with it.

Multigent accepts a code snippet and routes it through five specialised AI agents running concurrently. Each agent audits a different dimension of the code — security, bugs, performance, style, and overall quality. A sixth agent, the Review Leader, synthesises every report into a single executive-level document with an overall health score from 0 to 100.

---

## What Multigent does

**Submit** — paste any code snippet into the web interface. No repository access required; you control the scope by choosing what you paste.

**Analyse** — five agents fire simultaneously, each powered by Gemini 2.5 Flash:

| Agent | Responsibility |
|---|---|
| Security Analyzer | OWASP Top 10, hardcoded secrets, unsafe patterns, dependency risks |
| Bug Detector | Logic errors, edge-case failures, race conditions, dead code |
| Performance Profiler | Algorithmic complexity, blocking I/O, caching opportunities |
| Style Reviewer | Naming conventions, formatting, docstrings, code readability |
| Review Leader | Synthesises all findings, calculates the overall health score |

**Review** — results appear in a tabbed report interface. Each tab renders the agent's markdown output — summary tables, code snippets, before/after examples, and remediation steps. The health score (0–100) is displayed prominently and colour-coded green, amber, or red.

---

## Quickstart

### Production (recommended for evaluation)

```bash
git clone https://github.com/Huniity/multigent.git
cd multigent
make env        # then edit .env and add your GEMINI_API_KEY
make start-prod
```

Open **http://localhost:80** in your browser.

The production stack runs four services: PostgreSQL, Django (via Gunicorn), a built React frontend, and nginx as a reverse proxy on port 80. All API traffic is proxied through nginx; the frontend is served as pre-built static files.

> **Note:** `.env.example` must be present in the repository root. If it is missing, run `make env` to generate a `.env` file with default development values, then add your `GEMINI_API_KEY`.

### Development

The development stack mounts source directories as Docker volumes so that code changes are picked up without rebuilding.

```bash
git clone https://github.com/Huniity/multigent.git
cd multigent
make env                    # generates .env with dev defaults
# add GEMINI_API_KEY to .env
make start-dev
```

| Service | URL |
|---|---|
| Frontend (Vite HMR) | http://localhost:5173 |
| Backend (Django) | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/api/docs/ |
| Database admin | http://localhost:8080 |

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | **Yes** | Google AI API key for Gemini 2.5 Flash |
| `SECRET_KEY` | Yes | Django secret key |
| `POSTGRES_DB` | Yes | PostgreSQL database name |
| `POSTGRES_USER` | Yes | PostgreSQL username |
| `POSTGRES_PASSWORD` | Yes | PostgreSQL password |
| `DEBUG` | No | `True` for development, `False` for production |
| `ALLOWED_HOSTS` | No | Comma-separated list of allowed hostnames |
| `MODEL` | No | Gemini model string (default: `gemini-2.5-flash`) |

`make env` generates a `.env` file with sensible development defaults for everything except `GEMINI_API_KEY`, which must be added manually.

---

## Make targets

Run `make help` at any time to see all targets with descriptions.

### Environment & setup

| Target | Description |
|---|---|
| `make env` | Create `.env` with default development values if it does not exist |
| `make prepare` | Set up local Python 3.12 environment and sync dependencies via `uv` |
| `make requirements` | Regenerate `requirements.txt` from `pyproject.toml` |
| `make sync-dev` | Install frontend npm packages and sync backend Python dependencies |

### Running the stack

| Target | Description |
|---|---|
| `make up` | Build and start the production stack (nginx on port 80) |
| `make start-dev` | Build and start all services, wait for the database, run migrations, and prompt for a superuser — the recommended first-run command |
| `make up-dev` | Start the development stack (without the readiness check) |
| `make up-prod` | Build and start the production stack (nginx on port 80) |
| `make clean` | Stop all containers and remove volumes and orphaned services |

### Database

| Target | Description |
|---|---|
| `make migrate-dev` | Run Django migrations in the development stack |
| `make migrate-prod` | Run Django migrations in the production stack |
| `make migration-dev` | Create new migration files from model changes (development) |
| `make migration-prod` | Create new migration files from model changes (production) |
| `make superuser-dev` | Create a Django admin superuser (development) |
| `make superuser-prod` | Create a Django admin superuser (production) |

### Code quality

| Target | Description |
|---|---|
| `make check` | Lint Python code with Ruff |
| `make format` | Auto-format Python code with Ruff |
| `make fullCheck` | Run both `check` and `format` |
| `make pre-commit-all` | Run all pre-commit hooks across every file |

### Diagnostics

| Target | Description |
|---|---|
| `make check-dev` | Run Django system checks (development) |
| `make check-prod` | Run Django system checks (production) |
| `make logs-backend-dev` | Tail the Django application log (development) |
| `make logs-backend-prod` | Tail the Django application log (production) |
| `make logs-pytest-dev` | Print the pytest log (development) |
| `make logs-pytest-prod` | Print the pytest log (production) |

---

## Running tests

### Backend

```bash
make backend-test-dev
make backend-test-prod
```

The active test suite covers the context builder module
(`srcs/backend/agents_ai/github/test_context_builder.py`), with six
pytest cases validating both `build_context_from_file` and
`build_context_from_pasted_code` — including empty input handling,
correct bundle construction, and accurate `files_included` output.
Logs from each run are written to `/app/logs/pytest.log` inside the
container and can be read with `make logs-pytest-dev`.

### Frontend

```bash
make frontend-test
```

### All tests

```bash
make test
```

---



## Architecture

Multigent is a Docker Compose application with a Django REST backend, a React + TypeScript frontend, and a PostgreSQL database. The five AI agents run concurrently via a `ThreadPoolExecutor` inside a background thread, keeping the HTTP response time at a constant `202 Accepted` regardless of how long the crew takes.

```
Browser ──POST /api/reviews/──► Django ──► Background thread
                                  │                │
                              202 Accepted    ThreadPoolExecutor
                                             ├── Security Agent ──► Gemini API
                                             ├── Bug Agent      ──► Gemini API
                                             ├── Performance    ──► Gemini API
                                             └── Style Agent    ──► Gemini API
                                                      │
                                               Review Leader ──► Gemini API
                                                      │
                                                 PostgreSQL (ReviewResult)
                                                      │
Browser ──GET /api/reviews/:id/──► Django ──────────►┘
```

For the full system diagram, concurrency design rationale, token budget documentation, and data model reference, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Folder Architecture

```
multigent/
├── .devcontainer/
│   ├── devcontainer-lock.json
│   └── devcontainer.json
├── .editorconfig
├── .pre-commit-config.yaml
├── .python-version
├── CONTRIBUTORS.md
├── LICENSE
├── Makefile
├── README.md
├── ci.yaml
├── compose.prod.yaml
├── compose.yaml
├── ops/
│   ├── backend/
│   │   ├── Dockerfile
│   │   └── Dockerfile.prod
│   └── nginx/
│       └── nginx.conf
├── scripts/
│   └── trello_injection.py
└── srcs/
    ├── backend/
    │   ├── .gitignore
    │   ├── agents_ai/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── config/
    │   │   │   ├── agents.yaml
    │   │   │   └── tasks.yaml
    │   │   ├── crew.py
    │   │   ├── migrations/
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   ├── tests.py
    │   │   ├── tools/
    │   │   │   ├── __init__.py
    │   │   │   └── custom_tool.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── main.py
    │   ├── manage.py
    │   ├── multigent/
    │   │   ├── __init__.py
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── migrations/
    │   │   │   └── __init__.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── pyproject.toml
    │   ├── requirements.txt
    │   └── uv.lock
    └── frontend/
        ├── .gitignore
        ├── README.md
        ├── eslint.config.js
        ├── index.html
        ├── jsconfig.json
        ├── package-lock.json
        ├── package.json
        ├── public/
        │   ├── favicon.svg
        │   └── icons.svg
        ├── src/
        │   ├── App.tsx
        │   ├── assets/
        │   │   ├── hero.png
        │   │   ├── react.svg
        │   │   └── vite.svg
        │   ├── index.css
        │   ├── main.tsx
        │   └── vite-env.d.ts
        ├── tsconfig.app.json
        ├── tsconfig.json
        ├── tsconfig.node.json
        ├── vite-env.d.ts
        ├── vite.config.js
        └── vite.config.ts
```

## The role of AI in this project

Multigent reviews code with AI. It was also built with significant AI assistance at every layer — which makes it a fitting example of the kind of development workflow it is designed to support.

### Frontend

The majority of frontend — visual design language, component architecture, page implementations, loading states, and animation — was boiler-plated and then developed on top of it in collaboration with **Claude** over multiple sessoions. The design direction (dark terminal aesthetic, acid-lime accent, Syne + JetBrains Mono type pairing, sharp geometric forms) was originally conceived and refined iteratively through conversation. Individual pages (Login, Register, Home, Dashboard, Review) were produced as TypeScript + React components, with the auth store, token refresh utility, and routing logic all written with the assistance of AI.

### Backend

The backend team used AI assistance, specifically **Claude** and **Gemini**, across several areas of the Django and infrastructure work. Docker and Docker Compose configuration — including the multi-stage Dockerfile setup, the nginx reverse proxy configuration, and the production compose file — was drafted with AI help and iterated on from there. The pytest suite followed the same pattern: AI generated the boilerplate test structure which the team then extended with project-specific cases. CI/CD pipeline research and configuration was also AI-assisted. On the agent side, the CrewAI agent and task definitions (`agents.yaml`, `tasks.yaml`) — including role descriptions, goal prompts, backstories, and expected output formats for all five agents — were configured with AI assistance, then refined through testing against real code submissions.

### Documentation

The project's documentation — this README, [ARCHITECTURE.md](ARCHITECTURE.md), and the updated [CONTRIBUTORS.md](CONTRIBUTORS.md) — was written with the help of Claude to ensure structural and inherent consistency. The architecture document in particular required synthesising information spread across the Django backend, CrewAI configuration, Docker infrastructure, and frontend to produce accurate descriptions of concurrency design, token budget rationale, and the GitHub URL reader approach, all under human review and oversight.

### Development workflow

The team used AI assistance throughout the development process: for assistance in resolving merge conflicts, debugging Vite configuration inside a Docker-in-Docker dev container, writing and iterating on git commands during complex multi-branch rebase, and clarifying Django REST Framework patterns. The project's Trello board was managed with an injection script (`scripts/trello_injection.py`) designed to interface with AI-assisted task tracking.

### What this means

The AI agents in Multigent review code written by humans and AI alike. The codebase they analyse in production was itself written partly with AI assistance. This is deliberate: the team built a tool they needed, using the tools available to them, and documented honestly how those tools were used. We understand the importance of transparency about AI involvement in development, and we present it as fully and as clearly as possible: both in the product and in how it was made.

---

## Licence

See [LICENSE](LICENSE).
