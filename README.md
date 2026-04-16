# GitHub Copilot Workshop

A hands-on workshop to learn **GitHub Copilot** from beginner to
intermediate — inline completions, Copilot Chat, agent mode, custom
instructions, prompt files, custom agents, MCP servers, and the
Copilot Coding Agent — all exercised against a real Python FastAPI project.

## What You'll Learn

| # | Exercise | Topic |
|---|----------|-------|
| 1 | [Getting Started](exercises/01-getting-started.md) | Install, sign in, inline suggestions, Chat, Ask/Edit/Agent modes |
| 2 | [Custom Instructions](exercises/02-custom-instructions.md) | `.github/copilot-instructions.md`, path-scoped `.instructions.md` |
| 3 | [Settings & Permissions](exercises/03-settings-and-permissions.md) | `.vscode/settings.json`, content exclusion, model picker |
| 4 | [Agent Mode & Auto-Approve](exercises/04-agent-mode.md) | Multi-file edits, checkpoints, terminal auto-approve |
| 5 | [Prompt Files](exercises/05-prompt-files.md) | Reusable `/slash` commands in `.github/prompts/` |
| 6 | [Custom Agents](exercises/06-custom-agents.md) | Scoped personas in `.github/agents/` (formerly "chat modes") |
| 7 | [MCP Servers](exercises/07-mcp-servers.md) | Extending Copilot with external tools via `.vscode/mcp.json` |
| 8 | [Context Management](exercises/08-context-management.md) | `@workspace`, `#file`, `#selection`, `#codebase`, `#changes` |
| 9 | [Real-World Workflow](exercises/09-real-world-workflow.md) | End-to-end feature + Copilot Coding Agent on an issue |

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [Visual Studio Code](https://code.visualstudio.com/) with the **GitHub Copilot** and **GitHub Copilot Chat** extensions
- A GitHub account with an active Copilot subscription (Free, Pro, Business, or Enterprise)

Optional but referenced in some exercises:
- [GitHub CLI](https://cli.github.com/) with the Copilot extension (`gh extension install github/gh-copilot`)
- A fine-grained GitHub personal access token (for the GitHub MCP exercise)

## Quick Start

```bash
# Clone the repo
git clone https://github.com/zachschillaci27/github-copilot-workshop.git
cd github-copilot-workshop

# Install dependencies
uv sync

# Verify setup
uv run pytest

# Open in VS Code
code .
```

Then in VS Code:

1. Sign in to GitHub Copilot (status-bar icon → *Sign in*).
2. Open the Chat view (`Ctrl/Cmd+Alt+I`).
3. Ask: *"What does this project do?"* — Copilot will use the
   instructions in `.github/copilot-instructions.md` automatically.

## The Demo Project: TaskFlow API

A task-management REST API built with FastAPI. Small enough to read in a few
minutes, but with enough surface area to exercise every Copilot feature.

### Run the API
```bash
uv run uvicorn taskflow.main:app --reload
# Open http://localhost:8000/docs for interactive API docs
```

### Run Tests
```bash
uv run pytest                                          # all tests
uv run pytest tests/test_tasks.py -v                   # task tests only
uv run pytest tests/test_tasks.py::test_create_task -v # single test
```

### Project Structure
```
src/taskflow/
├── main.py              # FastAPI app entry point
├── models.py            # Pydantic request/response models
├── database.py          # In-memory database with seed data
├── utils.py             # Helper functions
└── routers/
    ├── tasks.py         # Task CRUD endpoints
    └── users.py         # User endpoints

tests/
├── conftest.py          # Shared fixtures
├── test_tasks.py        # Task endpoint tests
├── test_models.py       # Model validation tests
└── test_utils.py        # Utility function tests
```

### GitHub Copilot Configuration (included)
```
.github/
├── copilot-instructions.md         # Repo-wide project instructions
├── instructions/
│   ├── tests.instructions.md       # applyTo: tests/**/*.py
│   └── routers.instructions.md     # applyTo: src/taskflow/routers/**
├── prompts/
│   ├── add-endpoint.prompt.md      # /add-endpoint
│   ├── review.prompt.md            # /review
│   ├── test-coverage.prompt.md     # /test-coverage
│   ├── debug.prompt.md             # /debug
│   └── changelog.prompt.md         # /changelog
├── agents/
│   ├── planner.agent.md            # read-only planning agent
│   └── reviewer.agent.md           # structured code review
└── workflows/
    └── copilot-setup-steps.yml     # env setup for the Copilot Coding Agent

.vscode/
├── settings.json                   # Copilot enablement + terminal auto-approve
└── mcp.json                        # MCP server config (GitHub)
```

### Interop — Claude Code artifacts (optional)

Two Claude-specific files are **intentionally kept** to show how the same
project can be instrumented for multiple coding agents:

```
CLAUDE.md                           # Project instructions Claude Code reads
.claude/skills/add-endpoint/        # Single Claude skill kept as a side-by-side
                                    # reference to .github/prompts/add-endpoint.prompt.md
```

Copilot doesn't read these, and Claude doesn't read the `.github/` files —
but the two sets of instructions describe the *same* project, which makes it
easy to compare conventions side-by-side. See the table in
`.claude/skills/README.md` for a concept-by-concept mapping.

## Feature Coverage

This workshop covers the following GitHub Copilot features:

- **Custom instructions** — repo-wide and path-scoped (`applyTo` frontmatter)
- **Settings & enablement** — per-language toggle, content exclusion, auto-approve
- **Ask / Edit / Agent modes** — when to use each
- **Prompt files** — reusable `/slash` commands with `${input:…}` variables
- **Custom agents** (formerly "chat modes") — personas with scoped tools (planner, reviewer)
- **MCP servers** — extending Copilot with GitHub, filesystem, Playwright, etc.
- **Chat variables & participants** — `#file`, `#selection`, `#codebase`, `#changes`, `@workspace`, `@terminal`, `@github`
- **Built-in slash commands** — `/fix`, `/tests`, `/explain`, `/doc`, `/new`, `/clear`
- **Model picker** — choosing the right model for the job
- **Copilot Coding Agent** — issue-driven, PR-producing autonomous agent

## Resources

- GitHub Copilot docs: <https://docs.github.com/en/copilot>
- Copilot in VS Code: <https://code.visualstudio.com/docs/copilot/overview>
- Awesome Copilot (community catalog): <https://github.com/github/awesome-copilot>
