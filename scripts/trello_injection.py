

#!/usr/bin/env python3
"""
DevMate — Trello Sprint Board Injector
=======================================
Creates all lists, labels, and cards (with subtask checklists,
branch names, and commit messages) on an existing Trello board.
 
Usage:
    pip install requests
    python trello_inject.py
 
Then fill in the three variables below:
    TRELLO_API_KEY  — from https://trello.com/power-ups/admin
    TRELLO_TOKEN    — from the Token link on that same page
    BOARD_ID        — the XXXXXXXX part of your board URL
"""
 
import sys
import time
import requests
 
# ── Config ────────────────────────────────────────────────────────────────────
 
TRELLO_API_KEY = "08a9813a4f1eda6338c12d5e54cca0a8"
TRELLO_TOKEN   = "ATTA9f8138c1fe9a64d0299f130c70295c5bcfbdb0469526bee94c2caac9ef48ffb1A6913ECB"
BOARD_ID       = "G0iEa7is"
 
# ── Trello API base ────────────────────────────────────────────────────────────
 
BASE = "https://api.trello.com/1"
 
def q(extra: dict = None) -> dict:
    """Base query params with auth."""
    p = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    if extra:
        p.update(extra)
    return p
 
def get(path, **params):
    r = requests.get(f"{BASE}{path}", params=q(params))
    r.raise_for_status()
    return r.json()
 
def post(path, **data):
    r = requests.post(f"{BASE}{path}", params=q(), json=data)
    r.raise_for_status()
    time.sleep(0.3)  # stay under Trello rate limit (100 req/10s)
    return r.json()
 
def put(path, **data):
    r = requests.put(f"{BASE}{path}", params=q(), json=data)
    r.raise_for_status()
    time.sleep(0.3)
    return r.json()
 
# ── Labels ─────────────────────────────────────────────────────────────────────
# Trello colours: red, orange, yellow, green, blue, purple, pink, sky, lime, null
 
LABEL_DEFS = [
    ("Adrien",     "blue"),
    ("Diogo",      "green"),
    ("Giulio",     "orange"),
    ("Sprint 1",   "sky"),
    ("Sprint 2",   "purple"),
    ("Foundation", "null"),
    ("Auth",       "yellow"),
    ("GitHub API", "lime"),
    ("Context",    "pink"),
    ("Agents",     "red"),
    ("API",        "blue"),
    ("Frontend",   "orange"),
    ("CLI",        "sky"),
    ("Docs",       "lime"),
    ("CI/CD",      "purple"),
]
 
# ── Lists (columns) ────────────────────────────────────────────────────────────
 
LIST_NAMES = [
    "Sprint 1 — Week 1",
    "Sprint 2 — Week 2",
    "Adrien",
    "Diogo",
    "Giulio",
    "To-Do",
    "In Progress",
    "Code Review",
    "Approved",
    "Done",
]
 
# ── Tasks ──────────────────────────────────────────────────────────────────────
# Each task maps to:
#   list_name  → which Trello column the card lives in
#   labels     → list of label names to attach
#   checklist  → list of subtask strings shown inside the card
 
TASKS = [
    # ── SPRINT 1 ──────────────────────────────────────────────────────────────
    {
        "id": "F-01",
        "title": "Django project scaffold + settings split (base/dev/prod)",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Foundation"],
        "day": "Mon",
        "hours": 2,
        "branch": "chore/F-01-project-scaffold",
        "commit": "chore(project): initialise django project with settings split and ruff config",
        "checklist": [
            "django-admin startproject devmate backend/",
            "Create settings/base.py, settings/dev.py, settings/prod.py",
            "Configure INSTALLED_APPS, DB, and ALLOWED_HOSTS per env",
            "Add ruff.toml with lint rules",
            "Verify python manage.py check passes",
        ],
    },
    {
        "id": "F-02",
        "title": "requirements.txt + requirements-dev.txt",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Foundation"],
        "day": "Mon",
        "hours": 1,
        "branch": "chore/F-02-requirements",
        "commit": "chore(deps): add base and dev requirements files",
        "checklist": [
            "Add django, djangorestframework, simplejwt, psycopg2, httpx, crewai, google-generativeai",
            "Add pytest, pytest-django, ruff, pre-commit to dev requirements",
            "Pin all versions",
            "Verify pip install -r requirements.txt succeeds in container",
        ],
    },
    {
        "id": "F-03",
        "title": "Docker Compose dev + Dockerfiles (backend + frontend)",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "Foundation"],
        "day": "Mon",
        "hours": 3,
        "branch": "chore/F-03-docker-setup",
        "commit": "chore(docker): add dev compose with backend, frontend, db, adminer, nginx",
        "checklist": [
            "Write backend/Dockerfile (python:3.11-slim, install deps, run gunicorn)",
            "Write frontend/Dockerfile (node:20-alpine, vite build)",
            "Write docker-compose.yml with backend, frontend, db (postgres:16), adminer, nginx",
            "Map ports: 8000 backend, 5173 frontend, 5432 db, 8080 adminer, 80 nginx",
            "Add .env.example with all required env vars",
            "Test: make up boots all services cleanly",
        ],
    },
    {
        "id": "F-04",
        "title": "Makefile with all project targets",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "Foundation"],
        "day": "Mon",
        "hours": 2,
        "branch": "chore/F-04-makefile",
        "commit": "chore(make): add makefile with up, down, migrate, test, lint and shell targets",
        "checklist": [
            "make up → docker compose up --build",
            "make down → docker compose down",
            "make migrate → run django migrations inside container",
            "make test → pytest inside backend container",
            "make lint → ruff check + ruff format --check",
            "make format → ruff format",
            "make shell → django shell inside container",
            "make logs → tail all service logs",
            "make seed → load fixture data",
            "make prod-up → docker compose -f docker-compose.prod.yml up --build",
        ],
    },
    {
        "id": "F-05",
        "title": ".editorconfig + .pre-commit-config.yaml",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "Foundation"],
        "day": "Mon",
        "hours": 1,
        "branch": "chore/F-05-precommit",
        "commit": "chore(config): add editorconfig and pre-commit hooks with ruff",
        "checklist": [
            "Add .editorconfig (indent_style=space, indent_size=4, end_of_line=lf)",
            "Add .pre-commit-config.yaml with ruff, trailing-whitespace, end-of-file-fixer",
            "Run pre-commit install",
            "Verify hooks fire on git commit",
        ],
    },
    {
        "id": "F-06",
        "title": "Django app scaffold: app/ + agents_ai/",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "Foundation"],
        "day": "Mon",
        "hours": 1,
        "branch": "chore/F-06-app-scaffold",
        "commit": "chore(apps): scaffold app and agents_ai django apps",
        "checklist": [
            "python manage.py startapp app",
            "python manage.py startapp agents_ai",
            "Register both apps in settings/base.py INSTALLED_APPS",
            "Create app/urls.py and agents_ai/urls.py",
            "Wire up to devmate/urls.py under /api/v1/",
        ],
    },
    {
        "id": "DB-01",
        "title": "PostgreSQL models: User, Review, ReviewResult",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Foundation"],
        "day": "Tue",
        "hours": 2,
        "branch": "feat/DB-01-db-models",
        "commit": "feat(models): add user, review and reviewresult models with uuid primary keys",
        "checklist": [
            "Extend AbstractUser for custom User model (UUID pk, email unique)",
            "Create Review model (uuid, user FK, repo_url, owner, repo_name, status, health_score, timestamps)",
            "Create ReviewResult model (OneToOne → Review, bugs/security/performance/tech_debt/dependencies as JSONField)",
            "Add __str__ methods to all models",
            "Register models in admin.py",
        ],
    },
    {
        "id": "DB-02",
        "title": "Run and verify initial migrations",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Foundation"],
        "day": "Tue",
        "hours": 1,
        "branch": "feat/DB-02-migrations",
        "commit": "feat(db): create initial migrations for all models",
        "checklist": [
            "python manage.py makemigrations",
            "python manage.py migrate",
            "Verify tables exist in Adminer at localhost:8080",
            "Check migration files are committed to repo",
        ],
    },
    {
        "id": "GH-01",
        "title": "GitHub URL parser (owner + repo extractor)",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "GitHub API"],
        "day": "Tue",
        "hours": 1,
        "branch": "feat/GH-01-url-parser",
        "commit": "feat(github): add url parser to extract owner and repo from github urls",
        "checklist": [
            "Create agents_ai/github/parser.py",
            "Implement parse_github_url(url) → (owner, repo)",
            "Handle trailing slashes, .git suffixes, invalid URLs",
            "Raise ValueError with clear message on invalid input",
            "Write unit tests for valid + invalid cases",
        ],
    },
    {
        "id": "GH-02",
        "title": "Async httpx GitHub API client + repo tree fetcher",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "GitHub API"],
        "day": "Tue",
        "hours": 3,
        "branch": "feat/GH-02-api-client",
        "commit": "feat(github): add async httpx client with recursive tree fetcher",
        "checklist": [
            "Create agents_ai/github/client.py",
            "Implement get_default_branch(owner, repo) → str",
            "Implement get_file_tree(owner, repo) → list[dict] using ?recursive=1",
            "Handle 404 (repo not found) and 403 (rate limited) explicitly",
            "Add User-Agent header to all requests",
            "Write tests with mocked httpx responses",
        ],
    },
    {
        "id": "GH-03",
        "title": "Nginx config + frontend Vite scaffold",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "Foundation"],
        "day": "Tue",
        "hours": 3,
        "branch": "chore/GH-03-frontend-scaffold",
        "commit": "chore(frontend): scaffold vite react ts app with tailwind and nginx config",
        "checklist": [
            "npm create vite@latest frontend -- --template react-ts",
            "Install and configure Tailwind CSS",
            "Add React Router for page navigation",
            "Write nginx/nginx.conf (proxy /api/ to backend, serve frontend static)",
            "Verify nginx routes correctly in Docker Compose",
            "Add basic App.tsx with router placeholder",
        ],
    },
    {
        "id": "A-01",
        "title": "Register endpoint",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Auth"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/A-01-register",
        "commit": "feat(auth): add register endpoint with password hashing",
        "checklist": [
            "Create RegisterSerializer (email, username, password with validation)",
            "Create RegisterView (POST /api/v1/auth/register/)",
            "Hash password with make_password before saving",
            "Return 201 with user id and email on success",
            "Return 400 with field errors on duplicate email/username",
        ],
    },
    {
        "id": "A-02",
        "title": "Login endpoint + simplejwt tokens",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Auth"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/A-02-login-jwt",
        "commit": "feat(auth): add login endpoint with simplejwt access and refresh tokens",
        "checklist": [
            "Configure simplejwt in settings (ACCESS_TOKEN_LIFETIME=1h, REFRESH_TOKEN_LIFETIME=7d)",
            "Use TokenObtainPairView at POST /api/v1/auth/login/",
            "Use TokenRefreshView at POST /api/v1/auth/refresh/",
            "Test login returns access + refresh tokens",
            "Test invalid credentials returns 401",
        ],
    },
    {
        "id": "A-03",
        "title": "GET /auth/me/ + JWT guard",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Auth"],
        "day": "Wed",
        "hours": 1,
        "branch": "feat/A-03-jwt-guard",
        "commit": "feat(auth): add me endpoint and jwt permission class for protected routes",
        "checklist": [
            "Create MeView (GET /api/v1/auth/me/) returning current user info",
            "Set DEFAULT_AUTHENTICATION_CLASSES to JWTAuthentication in settings",
            "Set DEFAULT_PERMISSION_CLASSES to IsAuthenticated",
            "Verify unauthenticated request returns 401",
        ],
    },
    {
        "id": "GH-04",
        "title": "File scorer + relevance filter + token budget (300k)",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "GitHub API"],
        "day": "Wed",
        "hours": 3,
        "branch": "feat/GH-04-file-scorer",
        "commit": "feat(github): add file relevance scorer and 300k char token budget selector",
        "checklist": [
            "Implement score_file(path, size) → float with priority boosts and penalties",
            "Boost: main.py +10, models.py +8, auth.py +7, services.py +5",
            "Penalise: test_* -5, migrations/ -8, deeply nested >3 levels -2",
            "Implement select_files_by_budget(tree, contents, max_chars=300000)",
            "Always include README.md, requirements.txt, pyproject.toml regardless of score",
            "Write unit tests with known repo tree fixtures",
        ],
    },
    {
        "id": "GH-05",
        "title": "Concurrent file content fetcher (asyncio.gather)",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "GitHub API"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/GH-05-concurrent-fetcher",
        "commit": "feat(github): fetch selected files concurrently using asyncio.gather",
        "checklist": [
            "Implement fetch_file_content(owner, repo, path, client) → (path, str)",
            "Decode base64 content from GitHub API response",
            "Implement fetch_all_files(owner, repo, paths) using asyncio.gather",
            "Handle individual file 404s gracefully (skip, log warning)",
            "Write tests with mocked httpx responses for concurrent fetch",
        ],
    },
    {
        "id": "FE-01",
        "title": "Axios API client + JWT interceptor",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "Frontend"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/FE-01-api-client",
        "commit": "feat(frontend): add axios client with jwt interceptor and auto token refresh",
        "checklist": [
            "Create frontend/src/api/client.ts with axios instance",
            "Add request interceptor to attach Authorization: Bearer <token>",
            "Add response interceptor to refresh token on 401 and retry",
            "Store tokens in memory (not localStorage)",
            "Export typed functions: login(), register(), getMe()",
        ],
    },
    {
        "id": "A-04",
        "title": "Tests: full auth flow",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "Auth"],
        "day": "Thu",
        "hours": 3,
        "branch": "test/A-04-auth-tests",
        "commit": "test(auth): add tests for register, login, me endpoint and token validation",
        "checklist": [
            "test_register_success: 201 + user created in DB",
            "test_register_duplicate_email: 400 with error message",
            "test_login_success: 200 + access and refresh tokens returned",
            "test_login_wrong_password: 401",
            "test_me_authenticated: 200 + correct user data",
            "test_me_unauthenticated: 401",
            "test_token_refresh: new access token returned",
        ],
    },
    {
        "id": "CTX-01",
        "title": "AST parser: imports, functions, classes per .py file",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "Context"],
        "day": "Thu",
        "hours": 3,
        "branch": "feat/CTX-01-ast-parser",
        "commit": "feat(context): add ast parser to extract imports, functions and classes per file",
        "checklist": [
            "Create agents_ai/github/parser.py",
            "Implement parse_python_file(source: str) → dict",
            "Extract: imports (ast.Import + ast.ImportFrom)",
            "Extract: function names, args, docstrings, line numbers (ast.FunctionDef)",
            "Extract: class names, docstrings, line numbers (ast.ClassDef)",
            "Handle SyntaxError gracefully (return error key in dict)",
            "Write unit tests with known Python source fixtures",
        ],
    },
    {
        "id": "CTX-02",
        "title": "Metadata reader: README, requirements.txt, pyproject.toml",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "Context"],
        "day": "Thu",
        "hours": 1,
        "branch": "feat/CTX-02-metadata-reader",
        "commit": "feat(context): add metadata reader for readme, requirements and pyproject",
        "checklist": [
            "Extract README content (cap at 3000 chars)",
            "Extract raw requirements.txt content",
            "Extract pyproject.toml content if present",
            "Return dict with readme, dependencies, pyproject keys",
            "Handle missing files gracefully (empty string fallback)",
        ],
    },
    {
        "id": "FE-02",
        "title": "Login + Register pages",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "Frontend"],
        "day": "Thu",
        "hours": 3,
        "branch": "feat/FE-02-auth-pages",
        "commit": "feat(frontend): add login and register pages with client-side validation",
        "checklist": [
            "Create pages/Login.tsx with email + password form",
            "Create pages/Register.tsx with email, username, password form",
            "Add client-side validation (required fields, email format, password length)",
            "Store JWT tokens in React context / zustand on login",
            "Redirect to / on successful login",
            "Show API error messages inline below fields",
        ],
    },
    {
        "id": "V-01",
        "title": "POST /api/v1/reviews/ — submit repo URL",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "API"],
        "day": "Fri",
        "hours": 2,
        "branch": "feat/V-01-submit-review",
        "commit": "feat(reviews): add post reviews endpoint returning pending status with review id",
        "checklist": [
            "Create ReviewSubmitSerializer (repo_url with URL + github.com validation)",
            "Create ReviewCreateView (POST /api/v1/reviews/)",
            "Create Review DB record with status=pending",
            "Fire background thread to process the review",
            "Return 202 Accepted with review id, status, submitted_at",
        ],
    },
    {
        "id": "V-02",
        "title": "GET /api/v1/reviews/ — list user reviews",
        "list": "Sprint 1 — Week 1",
        "labels": ["Adrien", "Sprint 1", "API"],
        "day": "Fri",
        "hours": 1,
        "branch": "feat/V-02-list-reviews",
        "commit": "feat(reviews): add list reviews endpoint filtered by authenticated user",
        "checklist": [
            "Create ReviewListView (GET /api/v1/reviews/)",
            "Filter queryset by request.user",
            "Order by submitted_at descending",
            "Paginate results (page_size=20)",
            "Return id, repo_url, status, health_score, submitted_at per review",
        ],
    },
    {
        "id": "CTX-03",
        "title": "Context bundle builder",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "Context"],
        "day": "Fri",
        "hours": 2,
        "branch": "feat/CTX-03-bundle-builder",
        "commit": "feat(context): add context bundle builder merging ast, metadata and file tree",
        "checklist": [
            "Create agents_ai/github/bundle.py",
            "Implement build_bundle(owner, repo) → dict (async)",
            "Call: get_file_tree → score+filter → fetch_all_files → parse Python files → read metadata",
            "Collect all_imports and all_functions across parsed files",
            "Return full context bundle dict matching PLANNING.md schema",
            "Log bundle stats (total files, analysed files, total chars)",
        ],
    },
    {
        "id": "CTX-04",
        "title": "ProcessPoolExecutor for parallel AST parsing",
        "list": "Sprint 1 — Week 1",
        "labels": ["Diogo", "Sprint 1", "Context"],
        "day": "Fri",
        "hours": 2,
        "branch": "feat/CTX-04-multiprocessing",
        "commit": "feat(context): wrap ast parsing in processpoolexecutor for parallel execution",
        "checklist": [
            "Wrap parse_python_file calls in ProcessPoolExecutor(max_workers=4)",
            "Use executor.map over (path, source) pairs",
            "Ensure parse_python_file is importable at top level (required for pickling)",
            "Benchmark: compare sequential vs parallel parse time on 20 files",
            "Write test verifying parallel output matches sequential output",
        ],
    },
    {
        "id": "CI-01",
        "title": "GitHub Actions ci.yaml: lint + pytest",
        "list": "Sprint 1 — Week 1",
        "labels": ["Giulio", "Sprint 1", "CI/CD"],
        "day": "Fri",
        "hours": 2,
        "branch": "chore/CI-01-github-actions",
        "commit": "chore(ci): add github actions workflow with ruff lint and pytest on push",
        "checklist": [
            "Create .github/workflows/ci.yaml",
            "Trigger on push and pull_request to main",
            "Step: checkout code",
            "Step: set up Python 3.11",
            "Step: pip install -r requirements-dev.txt",
            "Step: ruff check . (lint)",
            "Step: ruff format --check . (format)",
            "Step: pytest (all tests)",
            "Add Python 3.12 to matrix",
        ],
    },
 
    # ── SPRINT 2 ──────────────────────────────────────────────────────────────
    {
        "id": "AG-01",
        "title": "BugDetector agent: definition + task builder",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Mon",
        "hours": 2,
        "branch": "feat/AG-01-bug-detector",
        "commit": "feat(agents): add bug detector agent definition and task builder with bundle injection",
        "checklist": [
            "Create agents_ai/agents/definitions.py",
            "Define BugDetectorAgent with role, goal, backstory targeting Gemini Flash 2.5",
            "Create build_bug_task(bundle) in agents_ai/agents/tasks.py",
            "Inject imports, function signatures, raw code into task description",
            "Define expected_output as strict JSON schema with findings array",
            "Test with a real bundle on a small public repo",
        ],
    },
    {
        "id": "AG-02",
        "title": "SecurityAudit agent: OWASP + secrets + unsafe calls",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Mon",
        "hours": 2,
        "branch": "feat/AG-02-security-agent",
        "commit": "feat(agents): add security audit agent covering owasp top 10 and unsafe calls",
        "checklist": [
            "Define SecurityAuditAgent (role: Senior AppSec Engineer)",
            "Build task: check OWASP Top 10, hardcoded secrets, eval/exec/pickle/os.system usage",
            "Include all_imports in task context so agent knows what libs are used",
            "Expected output: severity (high/medium/low), findings with file + line + recommendation",
            "Test with a repo known to have security issues",
        ],
    },
    {
        "id": "AG-03",
        "title": "PerformanceProfiler agent: O(n²) + bottlenecks",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Mon",
        "hours": 2,
        "branch": "feat/AG-03-performance-agent",
        "commit": "feat(agents): add performance profiler agent detecting algorithmic bottlenecks",
        "checklist": [
            "Define PerformanceProfilerAgent (role: Python Performance Expert)",
            "Build task: detect nested loops, O(n²) patterns, missing caching, blocking I/O",
            "Include radon complexity scores in task context",
            "Expected output: findings with pattern, file, line, description, suggestion",
            "Test with a repo containing obvious performance issues",
        ],
    },
    {
        "id": "V-03",
        "title": "Background task: full review pipeline",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Mon",
        "hours": 3,
        "branch": "feat/V-03-background-task",
        "commit": "feat(reviews): add background task orchestrating github read, bundle and agents",
        "checklist": [
            "Create app/tasks.py with process_review(review_id) function",
            "Set review.status = running at start",
            "Call build_bundle(owner, repo) from agents_ai",
            "Call run_analysis_crew(bundle) from agents_ai",
            "Call run_static_analysis(bundle) for tech debt + deps",
            "Save all results to ReviewResult model",
            "Calculate and save health_score",
            "Set review.status = complete (or failed on exception)",
            "Fire task in background thread from POST /reviews/ view",
        ],
    },
    {
        "id": "FE-03",
        "title": "Home page: repo URL submit form",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "Frontend"],
        "day": "Mon",
        "hours": 3,
        "branch": "feat/FE-03-home-page",
        "commit": "feat(frontend): add home page with repo url submit form and loading state",
        "checklist": [
            "Create pages/Home.tsx with GitHub URL input",
            "Validate URL format client-side before submitting",
            "Call POST /api/v1/reviews/ on submit",
            "Show loading spinner while waiting for 202 response",
            "On success: redirect to /review/:id",
            "Show error message on API failure",
        ],
    },
    {
        "id": "TD-01",
        "title": "TechDebt tracker (multiprocessing static analysis)",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Tue",
        "hours": 3,
        "branch": "feat/TD-01-tech-debt",
        "commit": "feat(analysis): add tech debt tracker with todo, dead code and complexity checks",
        "checklist": [
            "Create agents_ai/static_analysis/tech_debt.py",
            "Count TODO/FIXME/HACK comments using ast + regex",
            "Detect functions with no callers (basic dead code heuristic)",
            "Use radon cc to score cyclomatic complexity per function",
            "Flag functions with complexity > 10 as hotspots",
            "Run all checks in ProcessPoolExecutor across parsed files",
            "Return structured dict: todos, dead_code_files, complexity_hotspots",
        ],
    },
    {
        "id": "DEP-01",
        "title": "Dependency checker: CVEs + outdated packages",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Tue",
        "hours": 2,
        "branch": "feat/DEP-01-dep-checker",
        "commit": "feat(analysis): add dependency checker scanning requirements for cves and outdated packages",
        "checklist": [
            "Create agents_ai/static_analysis/dependencies.py",
            "Parse requirements.txt from bundle metadata",
            "Use pip-audit or safety to check for known CVEs",
            "Query PyPI JSON API for latest version per package",
            "Flag outdated packages (current version < latest)",
            "Return: total_checked, vulnerable list, outdated list, findings",
        ],
    },
    {
        "id": "AG-04",
        "title": "Crew runner: ThreadPoolExecutor for concurrent agents",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Tue",
        "hours": 2,
        "branch": "feat/AG-04-crew-runner",
        "commit": "feat(agents): add crew runner with threadpoolexecutor for concurrent agent calls",
        "checklist": [
            "Create agents_ai/agents/runner.py",
            "Implement run_analysis_crew(bundle) using ThreadPoolExecutor(max_workers=3)",
            "Submit bug, security, performance tasks concurrently",
            "Collect results with future.result() with timeout=120s",
            "Handle TimeoutError and agent exceptions gracefully",
            "Log time taken per agent and total wall time",
            "Return merged dict: bugs, security, performance",
        ],
    },
    {
        "id": "V-04",
        "title": "GET /reviews/{id}/ — full report",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Tue",
        "hours": 2,
        "branch": "feat/V-04-review-detail",
        "commit": "feat(reviews): add review detail endpoint returning full agent results",
        "checklist": [
            "Create ReviewDetailView (GET /api/v1/reviews/{id}/)",
            "Return 404 if review belongs to different user",
            "Include full ReviewResult data in response",
            "Include context_summary (file tree stats, imports)",
            "Return status=pending with empty results if not yet complete",
        ],
    },
    {
        "id": "V-05",
        "title": "GET /reviews/{id}/summary/ — health score only",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Tue",
        "hours": 1,
        "branch": "feat/V-05-review-summary",
        "commit": "feat(reviews): add review summary endpoint with health score and status",
        "checklist": [
            "Create ReviewSummaryView (GET /api/v1/reviews/{id}/summary/)",
            "Return: id, status, health_score, completed_at only",
            "Used by frontend for polling every 3 seconds",
        ],
    },
    {
        "id": "FE-04",
        "title": "Results page: poll + render agent cards",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "Frontend"],
        "day": "Tue",
        "hours": 3,
        "branch": "feat/FE-04-results-page",
        "commit": "feat(frontend): add results page with polling and collapsible agent result cards",
        "checklist": [
            "Create pages/Review.tsx that polls GET /reviews/:id/summary/ every 3s",
            "Stop polling when status = complete or failed",
            "Fetch full report from GET /reviews/:id/ when complete",
            "Create components/HealthScore.tsx (circular badge 0–100, colour coded)",
            "Create components/AgentResult.tsx (collapsible card per agent)",
            "Show findings list with severity badge, file, line, description per finding",
            "Handle status=failed with error message",
        ],
    },
    {
        "id": "H-01",
        "title": "Health score calculator (weighted formula 0–100)",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/H-01-health-score",
        "commit": "feat(reviews): add health score calculator using weighted agent findings",
        "checklist": [
            "Create app/scoring.py with calculate_health_score(results) → int",
            "Formula: start 100, -5 per bug (max -30), -10 per security issue (max -30)",
            "-3 per performance issue (max -15), -0.5 per TODO (max -10), -5 per CVE (max -15)",
            "Clamp result to 0–100",
            "Write unit tests with known inputs and expected scores",
        ],
    },
    {
        "id": "V-06",
        "title": "GET /reviews/history/?repo_url= — score trend",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/V-06-history",
        "commit": "feat(reviews): add history endpoint returning score trend for a repo url",
        "checklist": [
            "Create ReviewHistoryView (GET /api/v1/reviews/history/)",
            "Filter by repo_url query param + request.user",
            "Return list of: submitted_at, health_score, status ordered by date",
            "Used by frontend history page to show score over time",
        ],
    },
    {
        "id": "V-07",
        "title": "DRF serializers + input validation for all endpoints",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Wed",
        "hours": 1,
        "branch": "feat/V-07-serializers",
        "commit": "feat(api): add drf serializers with input validation for all endpoints",
        "checklist": [
            "Review all serializers for completeness",
            "Add URL validator to repo_url field (must start with https://github.com/)",
            "Add read_only_fields to prevent user from overwriting system fields",
            "Ensure all response serializers exclude sensitive fields",
        ],
    },
    {
        "id": "FE-05",
        "title": "HealthScore badge + History page",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "Frontend"],
        "day": "Wed",
        "hours": 3,
        "branch": "feat/FE-05-health-badge",
        "commit": "feat(frontend): add health score badge component and review history page",
        "checklist": [
            "HealthScore badge: green ≥80, yellow 50–79, red <50",
            "Create pages/History.tsx listing all past reviews",
            "Show repo name, date, health score, status per row",
            "Link each row to /review/:id results page",
            "Add nav bar with Home, History, Logout links",
        ],
    },
    {
        "id": "CLI-01",
        "title": "Typer CLI: review, history, report commands",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "CLI"],
        "day": "Wed",
        "hours": 2,
        "branch": "feat/CLI-01-typer-cli",
        "commit": "feat(cli): add typer cli with review, history and report commands",
        "checklist": [
            "Create backend/cli/main.py with typer.Typer()",
            "devmate review <github_url> → POST /reviews/, poll until complete, print summary",
            "devmate history → GET /reviews/, print table of past reviews",
            "devmate report <review_id> → GET /reviews/:id/, print full findings",
            "Store JWT token in ~/.devmate/config.json after login",
            "devmate login <email> → prompt password, save token",
            "Register CLI entry point in pyproject.toml",
        ],
    },
    {
        "id": "TST-01",
        "title": "Tests: GitHub reader (url, tree, scorer, fetcher)",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "GitHub API"],
        "day": "Thu",
        "hours": 2,
        "branch": "test/TST-01-github-tests",
        "commit": "test(github): add tests for url parser, tree fetcher and file scorer",
        "checklist": [
            "test_parse_github_url_valid: correct owner + repo extracted",
            "test_parse_github_url_invalid: ValueError raised",
            "test_get_file_tree: mocked httpx returns expected tree structure",
            "test_score_file: priority files score higher than test files",
            "test_select_files_by_budget: stays within 300k char cap",
            "test_fetch_all_files: concurrent fetch returns correct content per path",
        ],
    },
    {
        "id": "TST-02",
        "title": "Tests: context bundle + AST parser",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Context"],
        "day": "Thu",
        "hours": 2,
        "branch": "test/TST-02-bundle-tests",
        "commit": "test(context): add tests for ast parser and context bundle builder",
        "checklist": [
            "test_parse_python_file_imports: correct imports extracted",
            "test_parse_python_file_functions: function names + args + docstrings correct",
            "test_parse_python_file_syntax_error: error key returned, no exception raised",
            "test_build_bundle: mocked GitHub API returns correctly shaped bundle dict",
            "test_bundle_all_imports: imports correctly aggregated across files",
        ],
    },
    {
        "id": "TST-03",
        "title": "Tests: agents with mocked LLM calls",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Thu",
        "hours": 2,
        "branch": "test/TST-03-agent-tests",
        "commit": "test(agents): add agent tests with mocked llm calls and output schema assertions",
        "checklist": [
            "Mock CrewAI crew.kickoff() to return fixture JSON responses",
            "test_bug_detector_output_schema: response matches expected JSON structure",
            "test_security_agent_output_schema: severity field is high/medium/low",
            "test_performance_agent_output_schema: findings array present",
            "test_crew_runner_concurrent: all 3 futures resolve before timeout",
            "test_crew_runner_timeout: TimeoutError handled gracefully",
        ],
    },
    {
        "id": "TST-04",
        "title": "Tests: submit, poll, retrieve review flow",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Thu",
        "hours": 3,
        "branch": "test/TST-04-review-tests",
        "commit": "test(reviews): add integration tests for submit, poll and result retrieval flow",
        "checklist": [
            "test_submit_review_authenticated: 202 + review id returned",
            "test_submit_review_unauthenticated: 401",
            "test_submit_review_invalid_url: 400 with validation error",
            "test_get_review_pending: status=pending returned before processing",
            "test_get_review_complete: full results returned after mock processing",
            "test_get_review_other_user: 404 (cannot access another user's review)",
            "test_health_score_calculation: known inputs produce expected score",
            "test_list_reviews_only_own: other users' reviews not included",
        ],
    },
    {
        "id": "D-01",
        "title": "README.md: description, quickstart, Docker guide",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "Docs"],
        "day": "Thu",
        "hours": 2,
        "branch": "docs/D-01-readme",
        "commit": "docs(readme): add project description, quickstart guide and docker instructions",
        "checklist": [
            "Project description + what DevMate does",
            "Prerequisites: Docker, Docker Compose, make",
            "Quickstart: clone → cp .env.example .env → make up → open localhost:80",
            "All make targets explained",
            "How to run tests: make test",
            "How to use the CLI: devmate --help",
            "Architecture overview (brief, link to ARCHITECTURE.md)",
        ],
    },
    {
        "id": "D-02",
        "title": "CONTRIBUTORS.md + ARCHITECTURE.md",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "Docs"],
        "day": "Thu",
        "hours": 1,
        "branch": "docs/D-02-contributors-arch",
        "commit": "docs: add contributors file and architecture doc with system diagram",
        "checklist": [
            "CONTRIBUTORS.md: Adrien, Diogo, Giulio with roles and responsibilities",
            "ARCHITECTURE.md: system diagram (ASCII or Mermaid)",
            "Document concurrency design: why threading for agents, multiprocessing for parsing",
            "Document GitHub API reader approach and token budget logic",
        ],
    },
    {
        "id": "D-03",
        "title": "Docker prod Dockerfile + docker-compose.prod.yml",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "CI/CD"],
        "day": "Fri",
        "hours": 2,
        "branch": "chore/D-03-docker-prod",
        "commit": "chore(docker): add prod dockerfile and compose file for production deployment",
        "checklist": [
            "Write backend/Dockerfile.prod (multi-stage, no dev deps, gunicorn)",
            "Write frontend/Dockerfile with nginx serving built static files",
            "Write docker-compose.prod.yml (no adminer, no volume mounts, restart: always)",
            "Add nginx.conf for prod (gzip, security headers, proxy to gunicorn)",
            "Test: make prod-up boots and serves the app correctly",
        ],
    },
    {
        "id": "D-04",
        "title": "CI matrix: Python 3.11 + 3.12",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "CI/CD"],
        "day": "Fri",
        "hours": 1,
        "branch": "chore/D-04-ci-matrix",
        "commit": "chore(ci): add python version matrix for 3.11 and 3.12 in github actions",
        "checklist": [
            "Add strategy.matrix.python-version: [3.11, 3.12] to ci.yaml",
            "Ensure all tests pass on both versions",
            "Fix any version-specific issues found",
        ],
    },
    {
        "id": "D-05",
        "title": "REPORT.md: summary, challenges, decisions",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "Docs"],
        "day": "Fri",
        "hours": 2,
        "branch": "docs/D-05-report",
        "commit": "docs(report): add project report with challenges and concurrency design decisions",
        "checklist": [
            "What the project does (2 paragraphs)",
            "Architecture decisions: why Django, why CrewAI, why Gemini Flash 2.5",
            "Concurrency design: threading for agents, multiprocessing for AST, asyncio for GitHub API",
            "GitHub API reader: why no cloning, how token budget works",
            "Challenges faced and how they were solved",
            "Testing strategy: what is unit tested vs integration tested",
        ],
    },
    {
        "id": "TAG",
        "title": "Git tag v1.0.0 + zip upload before 23h59",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "CI/CD"],
        "day": "Fri",
        "hours": 0.5,
        "branch": "chore/TAG-v1-release",
        "commit": "chore(release): tag v1.0.0 for final submission",
        "checklist": [
            "git tag v1.0.0",
            "git push origin v1.0.0",
            "Create zip: git archive --format=zip HEAD -o devmate-v1.0.0.zip",
            "Upload zip to shared Google Drive folder",
            "Verify tag appears on GitHub",
        ],
    },
    {
        "id": "BUF-A",
        "title": "Buffer: Adrien — final fixes + polish",
        "list": "Sprint 2 — Week 2",
        "labels": ["Adrien", "Sprint 2", "API"],
        "day": "Fri",
        "hours": 1.5,
        "branch": "fix/BUF-A-polish",
        "commit": "fix(api): final polish and edge case fixes before submission",
        "checklist": [
            "Review all API responses match PLANNING.md schemas",
            "Check all error responses return consistent JSON format",
            "Verify Django admin works for all models",
            "Final make test — all tests passing",
        ],
    },
    {
        "id": "BUF-D",
        "title": "Buffer: Diogo — agent robustness",
        "list": "Sprint 2 — Week 2",
        "labels": ["Diogo", "Sprint 2", "Agents"],
        "day": "Fri",
        "hours": 2,
        "branch": "fix/BUF-D-agent-polish",
        "commit": "fix(agents): improve output parsing robustness for edge case llm responses",
        "checklist": [
            "Add JSON parsing fallback if agent returns malformed output",
            "Add retry logic (max 2 retries) for failed agent calls",
            "Test with a repo that has no Python files (graceful empty result)",
            "Test with a repo that has only 1 file",
        ],
    },
    {
        "id": "BUF-G",
        "title": "Buffer: Giulio — frontend polish + smoke test",
        "list": "Sprint 2 — Week 2",
        "labels": ["Giulio", "Sprint 2", "Frontend"],
        "day": "Fri",
        "hours": 1,
        "branch": "fix/BUF-G-frontend-polish",
        "commit": "fix(frontend): final ui polish and full docker stack smoke test",
        "checklist": [
            "Final UI pass: spacing, colours, loading states",
            "Test full flow end-to-end in Docker: register → login → submit repo → view results",
            "Verify make prod-up works cleanly from a fresh clone",
            "Check all pages are accessible and routes work",
        ],
    },
]
 
 
# ── Main injector ──────────────────────────────────────────────────────────────
 
def main():
    # Validate config
    if "YOUR_" in TRELLO_API_KEY or "YOUR_" in TRELLO_TOKEN or "YOUR_" in BOARD_ID:
        print("❌  Please fill in TRELLO_API_KEY, TRELLO_TOKEN, and BOARD_ID at the top of this file.")
        sys.exit(1)
 
    print(f"🚀  Starting DevMate Trello injection into board {BOARD_ID}")
    print()
 
    # ── 1. Create labels ──────────────────────────────────────────────────────
    print("🏷   Creating labels...")
    existing_labels = get(f"/boards/{BOARD_ID}/labels")
    label_map = {}
 
    for name, color in LABEL_DEFS:
        existing = next((l for l in existing_labels if l["name"] == name), None)
        if existing:
            label_map[name] = existing["id"]
            print(f"     ↳ Label '{name}' already exists, skipping")
        else:
            label = post(f"/boards/{BOARD_ID}/labels", name=name, color=color)
            label_map[name] = label["id"]
            print(f"     ↳ Created label '{name}' ({color})")
 
    print()
 
    # ── 2. Create lists (columns) ─────────────────────────────────────────────
    print("📋  Creating lists...")
    existing_lists = get(f"/boards/{BOARD_ID}/lists")
    list_map = {}
 
    for list_name in LIST_NAMES:
        existing = next((l for l in existing_lists if l["name"] == list_name), None)
        if existing:
            list_map[list_name] = existing["id"]
            print(f"     ↳ List '{list_name}' already exists, skipping")
        else:
            lst = post(f"/boards/{BOARD_ID}/lists", name=list_name, idBoard=BOARD_ID)
            list_map[list_name] = lst["id"]
            print(f"     ↳ Created list '{list_name}'")
 
    print()
 
    # ── 3. Create cards + checklists ──────────────────────────────────────────
    print(f"🃏   Creating {len(TASKS)} cards with checklists...")
    print()
 
    for i, task in enumerate(TASKS, 1):
        list_id = list_map.get(task["list"])
        if not list_id:
            print(f"     ⚠️  List '{task['list']}' not found for task {task['id']}, skipping")
            continue
 
        # Build card description
        desc = (
            f"**Day:** {task['day']}  |  "
            f"**Estimate:** {task['hours']}h\n\n"
            f"**Branch:**\n```\n{task['branch']}\n```\n\n"
            f"**Commit message:**\n```\n{task['commit']}\n```"
        )
 
        # Create card
        label_ids = [label_map[l] for l in task["labels"] if l in label_map]
        card = post(
            "/cards",
            idList=list_id,
            name=f"[{task['id']}] {task['title']}",
            desc=desc,
            idLabels=label_ids,
        )
        card_id = card["id"]
 
        # Create checklist
        checklist = post("/checklists", idCard=card_id, name="Subtasks")
        checklist_id = checklist["id"]
 
        for item in task["checklist"]:
            post(
                f"/checklists/{checklist_id}/checkItems",
                name=item,
                checked=False,
            )
 
        print(f"  [{i:02d}/{len(TASKS)}] ✅  {task['id']} — {task['title'][:55]}")
 
    print()
    print("🎉  Done! All cards injected into your Trello board.")
    print(f"    Open: https://trello.com/b/{BOARD_ID}")
 
 
if __name__ == "__main__":
    main()