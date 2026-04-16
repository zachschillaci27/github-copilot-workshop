---
name: add-endpoint
description: Scaffold a new API endpoint with tests
---

# Add New Endpoint

Create a new API endpoint matching the description the user provides.

## Steps

1. **Read existing patterns** - Look at `src/taskflow/routers/tasks.py` for the endpoint pattern
2. **Add the endpoint** to the appropriate router file
3. **Add database methods** if needed in `src/taskflow/database.py`
4. **Add Pydantic models** if needed in `src/taskflow/models.py`
5. **Write tests** in the appropriate test file
6. **Run tests** with `uv run pytest` to verify everything works
7. **Run linter** with `uv run ruff check src/ tests/` to check style

## Conventions (from CLAUDE.md)
- All endpoints under `/api/v1/`
- Use 201 for create, 204 for delete
- Return 404 with detail message for missing resources
- Query parameters for filtering
- Type hints on all functions
- Keep handlers thin - logic in database layer
