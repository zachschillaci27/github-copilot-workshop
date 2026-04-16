# TaskFlow API — Copilot Instructions

A Python FastAPI task-management API used as the training sandbox for this
GitHub Copilot workshop. These instructions are loaded automatically by
Copilot Chat, agent mode, and the Copilot Coding Agent for every request in
this workspace.

## Build & Run

- Install: `uv sync`
- Run server: `uv run uvicorn taskflow.main:app --reload`
- Run tests: `uv run pytest`
- Run single test: `uv run pytest tests/test_tasks.py::test_create_task -v`
- Lint: `uv run ruff check src/ tests/`
- Format: `uv run ruff format src/ tests/`

## Architecture

- `src/taskflow/main.py` — FastAPI app entry point
- `src/taskflow/models.py` — Pydantic request/response models
- `src/taskflow/database.py` — In-memory database with seed data
- `src/taskflow/routers/tasks.py` — Task CRUD endpoints
- `src/taskflow/routers/users.py` — User endpoints
- `src/taskflow/utils.py` — Helper functions
- `tests/` — Pytest test suite (use the `client` fixture from `conftest.py`)

## Code Conventions

- Type hints on every function signature
- Prefer `str | None` over `Optional[str]`
- Keep endpoint handlers thin — business logic lives in the database layer
- Sort imports with `ruff` (isort-compatible)
- Line length 88, Python 3.11+

## API Design

- All endpoints are under `/api/v1/`
- Use proper HTTP status codes (201 for create, 204 for delete)
- Return 404 with a `detail` message for missing resources
- Use query parameters for filtering, not request body

## Workshop Notes

- When asked to scaffold a new endpoint, mirror the pattern in
  `src/taskflow/routers/tasks.py` and add tests in `tests/`.
- This repo also ships a `CLAUDE.md` with overlapping content — it exists to
  demonstrate that the same project can be instrumented for both GitHub
  Copilot and Claude Code. Copilot reads this file; Claude Code reads
  `CLAUDE.md`. Keep them in sync when conventions change.
