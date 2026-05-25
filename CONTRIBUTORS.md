# Contributing to Multigent

## Team

| Contributor | Role | Responsibilities |
|---|---|---|
| Adrien | Project Lead · Django · Backend & Integration | Project direction, Django application architecture, REST API design, backend–frontend integration, deployment |
| Diogo | AI · CrewAI · Flow | Agent design and configuration, CrewAI crew and flow orchestration, LLM integration, context builder, concurrency strategy |
| Giulio | Frontend Design · Pages · Documentation | UI/UX design, React page implementation, auth flows, review interface, project documentation |

---

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multigent
   ```

2. **Create the environment file**
   ```bash
   make env
   ```
   Edit `.env` to add your `GEMINI_API_KEY` before starting.

3. **Start the development stack**
   ```bash
   make start-dev
   ```
   This builds all Docker services, waits for the database, runs migrations, and prompts for a superuser.

4. **Install local tooling** *(for linting/type-checking outside Docker)*
   ```bash
   make prepare
   ```
   Sets up Python 3.12, syncs dependencies via `uv`, and installs pre-commit hooks.

---

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | When to use |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that is neither a fix nor a feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `ci` | CI/CD configuration changes |
| `chore` | Dependency bumps or other housekeeping |

### Rules

- Use imperative mood: *"add feature"* not *"added feature"*
- Subject line under 50 characters, capitalised, no trailing period
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Reference issues with `Closes #123` in the footer

### Examples

```
feat(agents): run specialist agents concurrently via ThreadPoolExecutor

Previously agents ran sequentially, taking 4× longer. Now security,
bug, performance, and style agents fire in parallel and the review
leader synthesises their outputs afterward.

Closes #14
```

```
fix(auth): clear tokens on 401 refresh failure

If the refresh token is expired or invalid, the silent refresh in
authFetch now calls clearTokens() so ProtectedRoute redirects to
/login instead of looping.

Closes #31
```

```
docs: add ARCHITECTURE.md
```

---

## Pre-Commit Hooks

Pre-commit hooks run automatically before each commit. They are configured in `.pre-commit-config.yaml`.

| Hook | Purpose |
|---|---|
| `trailing-whitespace` | Removes trailing whitespace |
| `end-of-file-fixer` | Ensures files end with a single newline |
| `check-yaml` | Validates YAML syntax |
| `check-added-large-files` | Blocks files over 500 KB |
| `ruff-check` | Lints Python code |
| `ruff-format` | Auto-formats Python code |
| `mypy` | Static type checking |

Run all hooks manually:
```bash
make pre-commit-all
```

---

## Code Quality

### Python — Ruff

```bash
make check      # lint
make format     # auto-format
make fullCheck  # both
```

Default rules: **E/W** (pycodestyle), **F** (Pyflakes), **I** (isort).

### Python — mypy

```bash
uv run mypy .
```

Type hints are required on all public functions and class methods.

### TypeScript — ESLint

```bash
cd srcs/frontend && npm run lint
```

---

## Editor Configuration

`.editorconfig` enforces consistent style across editors.

| Scope | Setting |
|---|---|
| All files | Spaces, 4-space indent |
| `*.py` | 2-space indent |
| `package.json` | 1-space indent |

Install the [EditorConfig extension](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig) for VS Code.

---

## Development Workflow

```
1. git checkout -b feat/your-feature      # branch from dev
2. # make changes
3. make fullCheck                          # lint + format
4. uv run mypy .                          # type check
5. git add . && git commit -m "feat: …"  # pre-commit hooks run
6. git push origin feat/your-feature
7. Open a merge request into dev
```

---

## Dependencies

Managed with [uv](https://docs.astral.sh/uv/). See `srcs/backend/pyproject.toml`.

```bash
uv add package-name          # production
uv add --dev package-name    # development
make requirements            # regenerate requirements.txt
```

---

## Questions or Issues?

- Check existing issues and discussions on the repository
- Create a new issue for bugs or feature requests
- For minor fixes, a PR directly is fine

Thank you for contributing!