---
name: review
description: Review code for quality, security, and best practices
argument-hint: "[file-or-directory]"
allowed-tools: Read, Grep, Glob
model: sonnet
effort: high
---

# Code Review

Review $ARGUMENTS against the project's coding standards.

## Checklist

### Code Quality
- [ ] Type hints on all function signatures
- [ ] `str | None` used instead of `Optional[str]`
- [ ] Endpoint handlers are thin (logic in database layer)
- [ ] No duplicated code

### Security
- [ ] No hardcoded secrets or API keys
- [ ] User input is validated via Pydantic models
- [ ] Proper HTTP status codes used

### Testing
- [ ] Tests exist for new endpoints
- [ ] Both success and error cases tested
- [ ] Tests use the `client` fixture from `conftest.py`

### Style
- [ ] Imports sorted (ruff isort-compatible)
- [ ] Line length under 88 characters
- [ ] Docstrings on public functions

Provide feedback organized by severity:
1. **Critical** - Must fix before merge
2. **Important** - Should fix
3. **Suggestion** - Nice to have
