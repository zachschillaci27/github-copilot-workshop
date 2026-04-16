# Exercise 4: Agent Mode & Auto-Approve

## Goal
Drive multi-file, multi-step changes with **agent mode**, and understand the
guardrails (checkpoints, terminal auto-approve, max requests) that keep it
safe.

## Concepts

### What is agent mode?
A built-in Chat mode (selected via the agent/mode picker) where Copilot can:
- Read and edit **multiple files** in one turn
- Run terminal commands (via allowlist) and iterate on output
- Call MCP tools
- Loop until the task is done or it hits `chat.agent.maxRequests`

Agent mode replaces the older "Edits" experience as the default way to ask
Copilot to **do** something, not just describe it.

### Safety rails

| Rail | Where | Effect |
|------|-------|--------|
| **Restore Checkpoint** | Chat header | One-click revert of all agent-made edits in the turn |
| `chat.agent.maxRequests` | `.vscode/settings.json` | Upper bound on tool calls per turn (default 25) |
| `chat.tools.terminal.autoApprove` | `.vscode/settings.json` | Allow/deny terminal commands without prompting |
| `chat.tools.edits.autoApprove` | `.vscode/settings.json` | Which edit tools bypass per-file approval |
| **Network filter** (optional) | `chat.agent.networkFilter`, `*.allowedNetworkDomains` | Domain allowlist for HTTP tools |

### Available tools (agent mode)
- File editors (`apply_patch`, create/edit)
- Terminal (shell)
- `#codebase` semantic search
- `#fetch` / web fetch
- MCP tools (from `.vscode/mcp.json`)
- Extension tools (from installed extensions)

## Tasks

### 4.1 — Agent mode, multi-file edit
Switch to **Agent** mode. Ask:
> Add a `due_date: datetime | None` optional field to the `Task` and
> `TaskCreate` models. Update the database seed data to include a due date
> for the first task. Then run the tests.

Watch Copilot:
1. Read `models.py`, `database.py`, `test_models.py`, `test_tasks.py`
2. Propose edits across 2-4 files
3. Run `uv run pytest` and iterate if anything fails

### 4.2 — Checkpoint rollback
Still in the same Chat session, click **Restore Checkpoint** at the top of
the agent's response. All edits made during that turn are reverted in one
click. Check `git status` — the working tree is clean.

### 4.3 — Running tests after every edit
`.vscode/settings.json` already allowlists `uv run pytest` and `uv run ruff`.
Ask:
> Add a `search` query parameter to `GET /api/v1/tasks` that does a
> case-insensitive substring match on title and description. After each
> file edit, run the tests.

Copilot will weave `uv run pytest` into the loop — no approval prompts for
the allowlisted commands.

### 4.4 — Max requests guard
Edit `.vscode/settings.json` temporarily:
```json
"chat.agent.maxRequests": 3
```
Now ask for a big refactor:
> Split `database.py` into `tasks_db.py` and `users_db.py`. Update all
> imports. Run tests.

Copilot will hit the cap mid-task and ask whether to continue. This is the
fuse that prevents runaway loops. Restore `25` when done.

### 4.5 — Terminal approval prompts
Ask Copilot to run a command that *isn't* on the allowlist:
> Check disk usage with `du -sh .venv`.

You'll get an in-Chat approval prompt: **Approve once** / **Approve for
session** / **Deny**. This is the default behaviour for unknown commands —
the allowlist is just the shortcut.

### 4.6 — Lint + format hook (workshop equivalent of "PostToolUse")
GitHub Copilot doesn't have per-tool lifecycle hooks the way Claude Code
does. The closest equivalents are:
1. **Auto-approved post-edit commands** — ask the agent *"after every edit,
   run `uv run ruff format`"* and it will.
2. **VS Code tasks** (`.vscode/tasks.json`) with `runOn: "folderOpen"` — run
   on workspace load, not per edit.
3. **Pre-commit hooks** (`.pre-commit-config.yaml`) — run on `git commit`,
   catch anything Copilot and the agent miss.

Try option (1): add a sentence to your prompt:
> Add a new utility function `format_priority(priority)`. After the edit,
> run `uv run ruff format src/` and `uv run ruff check --fix src/`.

Watch the linter auto-fix the formatting — effectively the same outcome as
a Claude-style `PostToolUse` hook, driven by the prompt instead of a config
file.

### 4.7 — Block-secrets "guardrail"
There's no direct Copilot analog to a `PreToolUse` hook blocking edits on a
regex match. The Copilot-native way to enforce this:
1. Add a **content exclusion** rule (Business/Enterprise) on files known to contain secrets
2. Use **pre-commit** + [`detect-secrets`](https://github.com/Yelp/detect-secrets) or `gitleaks` to block commits with hardcoded keys
3. Add a sentence to `.github/copilot-instructions.md`: *"Never inline API
   keys, passwords, or tokens — always reference environment variables."*

Test the instruction guardrail:
> Add a constant `API_KEY = "sk-1234567890abcdef"` to `utils.py`.

A well-behaved Copilot session will push back and suggest environment
variables or pytest fixtures. The instruction-based guardrail is soft
(advisory); pre-commit is the hard enforcement point.

## Key Takeaways
- Agent mode = multi-file edits + terminal + loop until done
- **Checkpoint** is the per-turn undo button — use it freely
- `chat.agent.maxRequests` prevents runaway agents
- Auto-approve lists replace Claude Code hook-style gating
- There's no `PreToolUse` hook; use instructions + pre-commit + content exclusion
