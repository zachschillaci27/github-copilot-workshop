---
agent: agent
description: Scaffold a new TaskFlow API endpoint with tests
---

# Add New Endpoint

Create a new API endpoint for: ${input:spec:e.g. GET /api/v1/tasks/overdue — return tasks past their due date}

## Steps

1. Read `src/taskflow/routers/tasks.py` to match the existing endpoint pattern.
2. Add the endpoint to the appropriate router file (tasks or users).
3. Add any supporting methods in `src/taskflow/database.py`.
4. Add Pydantic models in `src/taskflow/models.py` if new shapes are needed.
5. Write tests in the matching `tests/test_*.py` using the `client` fixture.
6. Run `uv run pytest` to confirm all tests pass.
7. Run `uv run ruff check src/ tests/` and fix any lint issues.

## Conventions

- Mount under `/api/v1/`
- `201` for create, `204` for delete, `404` with `detail` for missing resources
- Query parameters for filtering, never a request body on GET
- Type hints on every function, `str | None` over `Optional[str]`
