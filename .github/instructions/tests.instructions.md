---
applyTo: "tests/**/*.py"
description: Pytest conventions for TaskFlow
---

# Test Conventions

- Use the `client` fixture from `tests/conftest.py` — do not instantiate
  `TestClient` directly in each test.
- Name tests `test_<action>_<scenario>` (e.g. `test_create_task_with_empty_title`).
- Every new endpoint needs at least:
  1. Happy path
  2. Validation / 4xx error path
  3. One edge case (empty input, max length, missing resource, etc.)
- Keep fixtures in `conftest.py`; avoid per-file fixture duplication.
- Prefer `response.json()` assertions over string matching on the raw body.
