---
mode: agent
description: Analyze test coverage and propose missing tests
---

# Test Coverage Analysis

Analyze test coverage for ${input:target:a file, directory, or leave blank for the whole project}.

## Steps

1. Run `uv run pytest -v` and note what's currently exercised.
2. Enumerate all endpoints in `src/taskflow/routers/`.
3. Enumerate all public methods in `src/taskflow/database.py`.
4. Enumerate all public functions in `src/taskflow/utils.py`.
5. Cross-reference against the test files in `tests/`.
6. Report gaps: untested functions and missing edge cases.

## Output

### Covered
List functions/endpoints that already have tests.

### Missing
List functions/endpoints without tests. For each, propose:
- Happy path
- Error cases
- Edge cases (empty input, max length, special characters)

### Suggested Test Code
Write the actual `pytest` functions that should be added — using the `client`
fixture from `tests/conftest.py`.
