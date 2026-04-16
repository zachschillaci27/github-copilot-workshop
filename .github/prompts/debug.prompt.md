---
mode: ask
description: Investigate a bug or error message
---

# Debug Investigation

Investigate this issue: ${input:issue:symptom, error message, or failing request}

## Steps

1. Use `#codebase` and grep to find code related to the symptom.
2. Read the relevant files end-to-end, not just the matching lines.
3. Trace the code path from the entry point (HTTP request, CLI call) through
   to where the failure occurs.
4. Identify the root cause.
5. Propose a minimal fix with specific file:line changes.

## Output Format

- **Symptom** — what the user sees
- **Root cause** — why it happens, citing file:line
- **Fix** — specific code changes needed
- **Prevention** — test or lint rule that would have caught this
