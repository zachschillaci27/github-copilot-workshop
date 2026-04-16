# Exercise 8: Context Management

## Goal
Control what Copilot sees — attach the right files, use chat variables and
participants effectively, and pick the right model for the turn.

## Concepts

### Chat variables (`#…`)
Inline references that inject specific context into the prompt.

| Variable | What it does |
|----------|--------------|
| `#file:<path>` | Attach a file (picker opens on `#file`) |
| `#selection` | The current editor selection |
| `#editor` | The currently open file |
| `#codebase` | Semantic search across the indexed repo |
| `#changes` | Source-control diff (working tree or staged) |
| `#problems` | Items from the VS Code Problems panel |
| `#terminalLastCommand` | Last terminal command + output |
| `#fetch` | Fetch a URL (with prompt) |
| `#todos` | Tracked implementation progress |

### Chat participants (`@…`)
Specialist subagents that know how to answer certain kinds of questions.

| Participant | Expertise |
|-------------|-----------|
| `@workspace` | Anything about this workspace (files, architecture, tests) |
| `@vscode` | VS Code features, settings, extensions |
| `@terminal` | Shell commands, terminal output |
| `@github` | Issues, PRs, repos on GitHub.com |

### `@workspace` vs `#codebase`
They sound similar and are easy to confuse:

- **`#codebase`** is a *tool* — a semantic search that returns ranked files
  and snippets. You drop it into any prompt.
- **`@workspace`** is a *participant* — a specialist that answers
  workspace-scoped questions and can itself call `#codebase` internally.

Rule of thumb: use `@workspace` when you're asking a question *about* the
project ("how does X work?"); use `#codebase` when you want to *attach*
semantically-relevant files to a more specific prompt.

### Model picker
Click the model name at the bottom of the Chat input. Tiers typically:
- **Fast / general** — default
- **Deep reasoning** — multi-step planning, complex refactors
- **Lightweight** — quick edits, high-volume completions
- **Vision** — image + code

Availability varies by plan (Free / Pro / Pro+ / Business / Enterprise).

## Tasks

### 8.1 — `#file` vs `#codebase`
Ask Copilot two versions of the same question:

**A.** With a specific file attached:
```
#file:src/taskflow/database.py
How does the task-filtering logic work?
```

**B.** With a codebase-wide search:
```
#codebase how does task-filtering work end-to-end from the HTTP request?
```

Compare answers: A is narrower and precise, B spans more files but may
include noise.

### 8.2 — `@workspace` deep-dive
Ask `@workspace`:
```
@workspace walk me through the data flow when a POST /api/v1/tasks request arrives.
```

Notice:
- It cites `path:line` references
- It handles routing across `routers/`, `database.py`, `models.py`
- It's smarter than a raw `#codebase` search for this kind of question

### 8.3 — `#changes` for review
Make a small change in `src/taskflow/utils.py`. Then ask:
```
#changes
What might be risky about this change? Suggest tests I should add.
```

Copilot gets the diff directly — no need to paste it.

### 8.4 — `#problems` for quick-fixes
Introduce a lint error on purpose: add an unused import to `main.py`. Open
the Problems panel (`Ctrl/Cmd+Shift+M`). Then ask:
```
#problems
Fix everything listed.
```

### 8.5 — `#terminalLastCommand`
Run a failing command in the integrated terminal:
```bash
uv run pytest tests/test_tasks.py::test_nonexistent_function
```
Then ask:
```
#terminalLastCommand
Why did this fail?
```

### 8.6 — `@github` for cross-repo context
With the GitHub MCP configured (Exercise 7) **or** the `@github` participant
available by default:
```
@github list the recent issues in this repo and summarise them
@github open a new issue: "Add pagination to task list endpoint"
```

### 8.7 — Model picker — same prompt, two models
Pick a deep-reasoning model, then a fast model, and run the same prompt:
```
Refactor database.py to split task and user operations into two modules
while preserving the public API and keeping all tests green.
```

Compare:
- Plan quality (did it think about module boundaries?)
- Speed
- Token usage (shown in the Chat status bar)

### 8.8 — Trim context before a long session
Long Chat sessions accumulate history. Two ways to keep things tight:

1. **`/clear`** — start a fresh session. Chat history is gone; workspace context (files, `#codebase`) is not affected.
2. **New chat tab** — hover the Chat title, click **+ New Chat**. Keeps previous tab around for reference.

Unlike Claude Code's `/compact`, Copilot Chat doesn't summarize history into
a running digest — it just trims from the top when the window fills. For
multi-phase tasks, `/clear` between phases is the cleanest pattern.

## Key Takeaways
- `#` = inline context variables (file, selection, codebase, changes, problems, terminal)
- `@` = participants (workspace, vscode, terminal, github)
- `#codebase` is a tool; `@workspace` is a specialist — use both
- Model picker trades latency for depth; default is fine for most turns
- `/clear` or new chat tab = Copilot's way to reset context between tasks
