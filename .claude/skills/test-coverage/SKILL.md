---
name: test-coverage
description: Analyze test coverage and suggest missing tests
argument-hint: "[file-or-directory, or blank for entire project]"
allowed-tools: Read, Grep, Glob, Bash
---

# Test Coverage Analysis

Analyze test coverage for: $ARGUMENTS (or entire project if not specified)

## Steps

1. **Run existing tests**: `uv run pytest -v` to see what passes
2. **Identify all endpoints** in `src/taskflow/routers/`
3. **Identify all database methods** in `src/taskflow/database.py`
4. **Identify all utility functions** in `src/taskflow/utils.py`
5. **Cross-reference with test files** in `tests/`
6. **Report gaps** - list untested functions and edge cases

## Output Format

### Covered
- List of functions/endpoints with existing tests

### Missing
- List of functions/endpoints WITHOUT tests
- For each, suggest specific test cases:
  - Happy path
  - Error cases
  - Edge cases

### Suggested Test Code
Write the actual test functions that should be added.
