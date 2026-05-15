# Contributing to Multi-Agent

We appreciate your interest in contributing! This guide outlines our development practices, code standards, and commit conventions.

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multigent
   ```

2. **Install dependencies**
   ```bash
   make prepare
   ```
   This will set up Python 3.12, sync dependencies, and install pre-commit hooks.

## Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages. This ensures clear, semantic versioning and automated changelog generation.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **refactor**: Code changes that neither fix bugs nor add features
- **perf**: Code changes that improve performance
- **test**: Adding or updating tests
- **ci**: Changes to CI/CD configuration
- **chore**: Other changes that don't modify src or test files (e.g., dependencies)

### Rules

- Use imperative mood ("add feature" not "added feature")
- Keep the subject line under 50 characters
- Capitalize the first letter
- Do not end the subject with a period
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Reference issues with `Closes #123` in the footer

### Examples

```
feat(agents): add multi-agent chat interface

Implements a new chat interface supporting concurrent agent execution
with real-time streaming responses.

Closes #42
```

```
fix(api): resolve authentication timeout issue

Previously, authentication tokens would expire during long-running
requests. Now tokens are refreshed automatically.

Closes #99
```

```
docs: update installation instructions
```

## Pre-Commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality. They are configured in `.pre-commit-config.yaml`.

### Enabled Hooks

1. **trailing-whitespace**: Removes trailing whitespace from files
2. **end-of-file-fixer**: Ensures files end with a single newline
3. **check-yaml**: Validates YAML syntax
4. **check-added-large-files**: Prevents committing large files (>500KB)
5. **ruff-check**: Lints Python code for errors and style issues
6. **ruff-format**: Automatically formats Python code
7. **mypy**: Performs static type checking on Python code

### Running Pre-Commit Checks

Check all files:
```bash
make pre-commit-all
```

Or run pre-commit on staged files:
```bash
pre-commit run
```

## Code Quality

### Ruff Configuration

We use [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and formatting. The project uses **default Ruff settings** with no custom overrides.

#### Default Enabled Rules

Ruff's default selection includes:
- **E/W (pycodestyle)**: PEP 8 style violations (indentation, whitespace, line length)
- **F (Pyflakes)**: Variable binding errors, unused imports, undefined names
- **I (isort)**: Import sorting and organization

#### Default Ignored Rules

- **Docstring rules (D)**: Not enabled by default
- **Pylint rules**: Not enabled by default
- **Type checking**: Not enabled by default (handled by mypy)

#### Ruff Commands

**Check for issues:**
```bash
make check
```
or
```bash
uv run ruff check
```

**Auto-format code:**
```bash
make format
```
or
```bash
uv run ruff format
```

**Check and format:**
```bash
make fullCheck
```

### Type Checking with mypy

mypy performs static type checking. Ensure type hints are present in your code:

```python
def add_numbers(a: int, b: int) -> int:
    return a + b
```

Type checking runs with pre-commit, but you can manually run:
```bash
uv run mypy .
```

## Editor Configuration

The project uses [EditorConfig](https://editorconfig.org/) to maintain consistent code style across editors. Configuration is in `.editorconfig`.

### Current Settings

```ini
[*]
indent_style = space
indent_size = 4

[*.py]
indent_size = 2

[package.json]
indent_size = 1
```

### What This Means

- **All files**: Use spaces (not tabs), 4-space indentation
- **Python files (*.py)**: Use 2-space indentation
- **package.json**: Use 1-space indentation

### Editor Support

EditorConfig is supported by most editors. Install the plugin for your editor:
- [VS Code](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig)
- [JetBrains IDEs](https://plugins.jetbrains.com/plugin/7294-editorconfig)
- [Vim](https://github.com/editorconfig/editorconfig-vim)
- [Sublime Text](https://github.com/sindresorhus/editorconfig-sublime)

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feat/your-feature-name
```

### 2. Make Your Changes
Follow the Editor Configuration settings and write tests.

### 3. Run Quality Checks
```bash
make fullCheck  # Runs ruff check and format
uv run mypy .   # Type checking
pytest          # Run tests
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat(scope): description"
```

Pre-commit hooks will automatically run. If they fail, fix issues and try again.

### 5. Push and Create a Pull Request
```bash
git push origin feat/your-feature-name
```

## Python Version

This project requires **Python 3.12 or later**. Make sure your environment uses the correct version:

```bash
python --version
```

## Dependencies

Dependencies are managed with [uv](https://docs.astral.sh/uv/). See `pyproject.toml` for current dependencies:

- **Core**: Django 6.0.5+, django-rest 0.8.7+
- **Dev**: pytest 9.0.3+, ruff 0.15.12+, typer 0.25.1+, mypy 1.20.2+

Add dependencies with:
```bash
uv add package-name        # Production
uv add --dev package-name  # Development
```

## Check trello for daily tasks
- https://trello.com/b/G0iEa7is/multigent

## Questions or Issues?

- Check existing issues and discussions
- Create a new issue for bugs or feature requests
- For minor issues, feel free to submit a PR directly

Thank you for contributing! 🎉
#### This markdown file was created in collab with AI Agents.
