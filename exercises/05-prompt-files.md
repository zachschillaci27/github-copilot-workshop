# Exercise 5: Prompt Files (Slash Commands)

## Goal
Package repeatable workflows as `/slash` commands using prompt files.

## Concepts

### What are prompt files?
Markdown files with YAML frontmatter that define a reusable prompt. They
appear in the Chat's slash-command menu (`/name`) and can be invoked from
anywhere.

### Location
```
.github/prompts/<name>.prompt.md        # Workspace (shared via git)
# or VS Code user profile for personal prompt files
```

The location is configurable via the `chat.promptFilesLocations` VS Code
setting.

### Frontmatter

| Field | Purpose |
|-------|---------|
| `description` | Shown in the slash-command menu |
| `agent` | `ask`, `agent`, `plan`, or the name of a custom agent (Exercise 6) |
| `tools` | (optional) Allow-list of tools; when set, `agent:` defaults to `agent` |
| `model` | (optional) Pin a specific model |
| `name` | (optional) Slash-command name; defaults to filename |
| `argument-hint` | (optional) Placeholder text in the slash menu |

> **Note on the field name.** VS Code used to call this `mode:` — it's now
> `agent:` (the rename happened alongside the chat-modes → custom-agents
> rename in early 2026). The legacy `mode:` value `edit` was consolidated
> into `agent`.

### Variables
- `${selection}` — the current editor selection
- `${file}` — the active file
- `${workspaceFolder}` — repo root
- `${input:variableName}` — prompt the user for input
- `${input:variableName:placeholder}` — prompt with a placeholder hint

### Dynamic context
Use chat variables inside the prompt body:
- `#codebase` — semantic search
- `#changes` — working-tree diff
- `#terminalLastCommand` — last shell output
- `#file:<path>` — attach a specific file

## Tasks

### 5.1 — Use the pre-built prompt files
This repo ships five:
```
/review             # review code against project standards
/test-coverage      # find untested code
/add-endpoint       # scaffold a new endpoint
/debug              # investigate an error
/changelog          # generate a changelog entry
```

Try each:
```
/review src/taskflow/routers/tasks.py
/test-coverage src/taskflow/routers/users.py
/add-endpoint GET /api/v1/tasks/overdue — return tasks past their due date
/debug GET /api/v1/tasks returns 500 when filtering by invalid status
/changelog
```

Each prompts the user for its `${input:…}` values if you don't include them
inline.

### 5.2 — Open one up and walk through the structure
```bash
cat .github/prompts/add-endpoint.prompt.md
```

Notice:
- `agent: agent` — this one needs to edit files and run tests
- `${input:spec:…}` — the first placeholder becomes a labeled form field
- The body is plain Markdown, readable as documentation too

### 5.3 — Create a "refactor" prompt
Create `.github/prompts/refactor.prompt.md`:
```markdown
---
agent: agent
description: Refactor the current selection against project conventions
---

Refactor the following code to match the project's conventions
(`.github/copilot-instructions.md`):

${selection}

## Requirements
- Preserve observable behaviour (tests must still pass)
- Use `str | None` instead of `Optional[str]`
- Keep endpoint handlers thin — move logic into `database.py`
- Add type hints if missing

After refactoring, run `uv run pytest` to confirm no regressions.
```

Select a function in `src/taskflow/routers/tasks.py` and run `/refactor`.

### 5.4 — Dynamic context with `#changes`
Create `.github/prompts/commit-message.prompt.md`:
```markdown
---
agent: ask
description: Suggest a conventional-commit message for the current diff
---

Suggest a commit message for the changes below. Use the
conventional-commits format (`type(scope): subject`).

#changes

Rules:
- One-line subject, ≤ 72 characters
- Optional body with wrapped lines at 72 chars
- Types: feat, fix, refactor, test, docs, chore, perf
```

Make a small change, then run `/commit-message`. Copilot ingests `#changes`
automatically.

### 5.5 — Scoped-tool prompt
Create `.github/prompts/doc-only.prompt.md`:
```markdown
---
agent: agent
description: Add docstrings without changing any logic
tools: ['search/codebase', 'edit']
---

Add Google-style docstrings to every public function in ${input:target:a file path}.

Rules:
- Do not modify function signatures or behaviour
- Only add or update docstrings
- Run `uv run pytest` at the end to confirm nothing broke
```

The restricted `tools` list keeps the agent from running arbitrary terminal
commands — only codebase search + file edit.

> Tool IDs use the namespaced form (`search/codebase`, `search/usages`,
> `web/fetch`, `edit`, `read/terminalLastCommand`, `agent`, …). Open VS
> Code's Chat → **Configure Tools** picker to see the current authoritative
> list; VS Code silently ignores IDs it doesn't recognise.

### 5.6 — Interop with Claude Code skills
Open the side-by-side:
```bash
cat .github/prompts/add-endpoint.prompt.md
cat .claude/skills/add-endpoint/SKILL.md
```

Same intent, two flavours:

| Copilot prompt file | Claude Code skill |
|---------------------|-------------------|
| `.github/prompts/<name>.prompt.md` | `.claude/skills/<name>/SKILL.md` |
| `agent: agent` | (implicit — agent chosen by model) |
| `tools: [...]` | `allowed-tools: …` |
| `${input:name}` | `$ARGUMENTS` |
| `#changes`, `#codebase` | `` !`git diff` ``, `Grep`, `Glob` |

Keeping both lets you run the same repo through either tool.

## Key Takeaways
- Prompt files = reusable `/slash` commands in `.github/prompts/`
- Frontmatter field is `agent:` (was `mode:`); values are `ask | agent | plan | <custom-agent-name>`
- `${input:name:placeholder}` and chat variables (`#file`, `#changes`, `#codebase`) inject dynamic context
- `tools: [...]` restricts what the prompt is allowed to do — use namespaced IDs (`search/codebase`, `edit`, `web/fetch`, …)
- Concept maps closely to Claude Code skills — identical idea, different file layout
