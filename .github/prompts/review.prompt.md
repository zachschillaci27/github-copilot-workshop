---
mode: ask
description: Review code against TaskFlow standards
---

# Code Review

Review the code in ${input:target:path or #file reference} against the project's
conventions (see `.github/copilot-instructions.md`).

## Checklist

### Quality
- [ ] Type hints on all function signatures
- [ ] `str | None` instead of `Optional[str]`
- [ ] Endpoint handlers are thin — logic in `database.py`
- [ ] No duplicated code

### Security
- [ ] No hardcoded secrets or API keys
- [ ] User input validated via Pydantic
- [ ] Proper HTTP status codes

### Tests
- [ ] Tests exist for new endpoints
- [ ] Happy path + error path + one edge case
- [ ] Uses the `client` fixture from `conftest.py`

### Style
- [ ] Imports sorted (ruff / isort)
- [ ] Lines ≤ 88 chars
- [ ] Docstrings on public functions

## Output Format

Group findings by severity:

1. **Critical** — must fix before merge
2. **Important** — should fix
3. **Suggestion** — nice to have

End with a single-line verdict: `APPROVE`, `REQUEST CHANGES`, or `NEEDS DISCUSSION`.
