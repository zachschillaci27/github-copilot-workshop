# TaskFlow API

> **Interop note** — this workshop is primarily oriented around **GitHub
> Copilot** (see `.github/copilot-instructions.md`). This `CLAUDE.md` is kept
> alongside it to demonstrate that the same project can be instrumented for
> multiple coding agents with minimal duplication: Copilot reads
> `.github/copilot-instructions.md`, Claude Code reads `CLAUDE.md`, and some
> tools also recognise `AGENTS.md`. Keep conventions in sync across files.

A Python FastAPI task management API used as the training sandbox for the
GitHub Copilot workshop (and optionally Claude Code).

## Build & Run

- Install: `uv sync`
- Run server: `uv run uvicorn taskflow.main:app --reload`
- Run tests: `uv run pytest`
- Run single test: `uv run pytest tests/test_tasks.py::test_create_task -v`
- Lint: `uv run ruff check src/ tests/`
- Format: `uv run ruff format src/ tests/`

## Architecture

- `src/taskflow/main.py` - FastAPI app entry point
- `src/taskflow/models.py` - Pydantic request/response models
- `src/taskflow/database.py` - In-memory database with seed data
- `src/taskflow/routers/tasks.py` - Task CRUD endpoints
- `src/taskflow/routers/users.py` - User endpoints
- `src/taskflow/utils.py` - Helper functions
- `tests/` - Pytest test suite

## Code Conventions

- Use type hints on all function signatures
- Prefer `str | None` over `Optional[str]`
- Keep endpoint handlers thin - business logic goes in database layer
- Tests use the `client` fixture from `conftest.py` (use `empty_db` when you
  need a database with no seed data)
- Sort imports with `ruff` (isort-compatible)
- Line length 88, Python 3.11+

## API Design

- All endpoints are under `/api/v1/`
- Use proper HTTP status codes (201 for create, 204 for delete)
- Return 404 with detail message for missing resources
- Use query parameters for filtering, not request body

## Workshop Notes

- When asked to scaffold a new endpoint, mirror the pattern in
  `src/taskflow/routers/tasks.py` and add tests in `tests/`.
- See the **Interop note** at the top for the relationship with
  `.github/copilot-instructions.md` — keep both in sync when conventions
  change.
