# multigent
An AI Council ready to analyze your codebase


```
User POSTs { "repo_url": "https://github.com/user/repo" }
        │
        ▼
1. Repo Cloner (async background task)
        │  git clone → temp folder on server
        ▼
2. Context Builder Service (multiprocessing)
        │
        ├── Process 1: File tree scanner (what files exist, languages detected)
        ├── Process 2: Code parser (ast → extracts imports, functions, classes)
        ├── Process 3: Static analysis (radon complexity, flake8 lint)
        └── Process 4: Metadata reader (README, requirements.txt, .env.example)
        │
        ▼
3. Context Bundle (structured dict saved to DB)
        {
          "language": "python",
          "file_tree": ["app/main.py", "app/models.py", ...],
          "imports": ["fastapi", "sqlalchemy", "requests", ...],
          "functions": [{"name": "get_user", "args": [...], "docstring": "..."}],
          "classes": [...],
          "readme": "This project does...",
          "dependencies": {"fastapi": "0.100.0", ...},
          "complexity_scores": {"app/main.py": 4.2, ...},
          "lint_issues": [...],
          "full_code_by_file": {"app/main.py": "...", ...}
        }
        │
        ▼
4. CrewAI Agents (ThreadPoolExecutor — all fire concurrently)
        │
        ├── Thread 1 → BugDetectorAgent     receives bundle
        ├── Thread 2 → SecurityAgent        receives bundle
        ├── Thread 3 → StyleAgent           receives bundle
        ├── Thread 4 → READMEGeneratorAgent receives bundle
        └── Thread 5 → FeaturePlannerAgent  receives bundle
        │
        ▼
5. Results merged → saved to DB → returned to user
        │
        ▼
6. Temp clone deleted from server

```