# Exercise 2: Custom Instructions

## Goal
Understand how `.github/copilot-instructions.md` and path-scoped
`.instructions.md` files give Copilot persistent context about your project.

## Concepts

### What are custom instructions?
Markdown files Copilot auto-loads for every chat / agent request in this
workspace. They tell Copilot about your stack, conventions, architecture,
and anything you don't want to repeat in every prompt.

### Three classes of instruction files

| Scope | Path | Shared via |
|-------|------|-----------|
| Repo-wide | `.github/copilot-instructions.md` | Git |
| Path-scoped | `.github/instructions/<name>.instructions.md` (frontmatter `applyTo:`) | Git |
| Personal | User profile (set via Command Palette → *Chat: Configure Chat Instructions*) | Not shared |

### Frontmatter (path-scoped only)
```yaml
---
applyTo: "tests/**/*.py"           # glob(s); comma-separated list supported
description: "Pytest conventions"  # shown in UI
---
```

> Important: these files influence **chat and agent** responses — they do
> **not** affect inline (ghost-text) suggestions.

## Tasks

### 2.1 — Read the existing instructions
```bash
cat .github/copilot-instructions.md
```

Open the Chat view and ask:
> What are the project's code conventions?

Notice Copilot answers from the instructions without reading any source
files.

### 2.2 — Test instruction effectiveness
Switch to **Agent** mode and ask:
> Create a new utility function called `format_task_id` that takes an
> integer and returns a string like `TASK-001`.

Check that Copilot follows the conventions:
- Type hints? ✓/✗
- Placed in `src/taskflow/utils.py`? ✓/✗
- `str | None` instead of `Optional[str]` if nullability appears? ✓/✗

### 2.3 — Add a new convention
Edit `.github/copilot-instructions.md` and append:
```markdown
## Error Handling
- Raise `HTTPException` from FastAPI for error responses
- Always include a `detail` field with a human-readable message
- Log errors via `logger = logging.getLogger(__name__)`
```

Now ask Copilot:
> Add error logging to the task creation endpoint.

Does it follow your new convention?

### 2.4 — Path-scoped instructions
Inspect the existing path-scoped file:
```bash
cat .github/instructions/tests.instructions.md
```

Note the `applyTo: "tests/**/*.py"` frontmatter. Copilot will only include
this file's content when the conversation involves files matching that glob.

**Try it:**
1. Open `tests/test_tasks.py` and ask: *"Add a test for deleting a non-existent task."* — the test conventions should show up in the response.
2. Open `src/taskflow/main.py` and ask: *"Add a new route."* — the test-specific rules should **not** appear.

### 2.5 — Create your own scoped file
Create `.github/instructions/database.instructions.md`:
```markdown
---
applyTo: "src/taskflow/database.py"
description: In-memory database conventions
---

# Database Conventions

- Every public method returns fully-hydrated Pydantic models, never raw dicts.
- Missing resources raise `KeyError` — routers translate to `HTTPException(404)`.
- Keep methods synchronous (we don't use `async def` here yet).
- Use UUID4 for new IDs (`str(uuid.uuid4())`).
```

Open `database.py` and ask Copilot to add a new method. Does it follow the rules?

### 2.6 — Bootstrap a new repo with `/new` + `/setup`
In the Chat view, type `/` and look for **`/new`** — it scaffolds new files
or workspaces from a natural-language description. For an existing repo
without instructions, you can ask:
> Generate a `.github/copilot-instructions.md` for this project by reading
> the code.

Copilot will inspect the repo and propose a draft instructions file.

### 2.7 — Interop with Claude Code
This repo also ships a top-level `CLAUDE.md`. Open both:
```bash
diff CLAUDE.md .github/copilot-instructions.md
```
Notice they describe the same project. Copilot reads
`.github/copilot-instructions.md`; Claude Code reads `CLAUDE.md`. Keeping
the two in sync is the simplest interop story. Some teams prefer a single
`AGENTS.md` file with symlinks or a build step to derive both.

## Key Takeaways
- `.github/copilot-instructions.md` is the most impactful file for team-wide Copilot productivity
- Path-scoped `.instructions.md` files (`applyTo:`) inject rules only where relevant
- Instructions influence chat/agent, **not** inline completions
- Keep `CLAUDE.md` / `.github/copilot-instructions.md` / `AGENTS.md` in sync when you support multiple agents
