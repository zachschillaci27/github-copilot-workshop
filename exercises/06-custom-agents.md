# Exercise 6: Custom Agents (formerly Chat Modes)

## Goal
Build scoped AI personas (planner, reviewer, doc-writer, …) using **custom
agents** — Copilot's equivalent of Claude Code subagents.

> **Rename in early 2026.** VS Code renamed "custom chat modes" to
> "custom agents". If you find `*.chatmode.md` files or the setting
> `chat.modeFilesLocations` online, those are the legacy form; rename them
> to `*.agent.md` and move them to `.github/agents/`.

## Concepts

### What are custom agents?
Markdown files that define a persistent chat persona with:
- A **system prompt** (body of the markdown)
- A scoped **tool allowlist** (`tools:` frontmatter)
- Optional **model pin** (`model:` frontmatter)
- A description shown in the agent picker

Once created, they sit alongside the built-in **Ask** and **Agent** agents
in the Chat's agent picker at the bottom of the input box.

### Location
```
.github/agents/<name>.agent.md       # Workspace (shared via git)
.claude/agents/<name>.md             # Also recognised (cross-tool interop)
~/.copilot/agents/<name>.agent.md    # User profile (personal)
```

Configurable via `chat.agentFilesLocations` in `settings.json`.

### Frontmatter

| Field | Purpose |
|-------|---------|
| `description` | Shown in the agent picker |
| `tools` | Array of allowed tool IDs (namespaced) |
| `model` | (optional) Pin a single model or a prioritised array |
| `name` | (optional) Display name; defaults to filename |
| `argument-hint` | (optional) Placeholder text |
| `agents` | (optional) Which sub-agents this agent may invoke (`*` for all) |

### Tool IDs — use the namespaced form

The current docs ship with names like:

| Tool ID | Purpose |
|---------|---------|
| `search/codebase` | Semantic repo search |
| `search/usages` | Symbol usages |
| `web/fetch` | HTTP fetch |
| `edit` | File edit tool |
| `read/terminalLastCommand` | Last terminal command + output |
| `agent` | Invoke a sub-agent |
| `<mcp-server>/*` | All tools from a configured MCP server |

> Open **Chat → Configure Tools** in VS Code to see the authoritative
> current list. VS Code silently ignores IDs it doesn't recognise, so if a
> tool name looks wrong in your agent file, the feature will just go
> missing.

## Tasks

### 6.1 — Try the pre-built agents
Open the agent picker at the bottom of the Chat view. Next to **Ask** and
**Agent**, you'll see **Planner** and **Reviewer**.

**Switch to Planner** and ask:
> How would you refactor `database.py` to split task and user operations into
> separate modules while preserving the public API?

Notice:
- The response is a structured **plan**, not a diff
- Copilot cites `path:line` references
- It asks clarifying questions when the request is ambiguous

**Switch to Reviewer** and ask:
> Review the changes we've made so far. Attach #changes.

You'll get structured output with **Critical / Important / Suggestions**
sections and a verdict — because the agent's system prompt mandates that
format.

### 6.2 — Inspect the agent files
```bash
cat .github/agents/planner.agent.md
cat .github/agents/reviewer.agent.md
```

Point at:
- `tools:` — only `search/codebase`, `search/usages`, `web/fetch` — no
  `edit` and no terminal-run tool, so these agents **can't** modify anything.
  That's the enforcement mechanism (not the system prompt).
- The body — it's just a Markdown system prompt.

### 6.3 — Create a test-writer agent
Create `.github/agents/test-writer.agent.md`:
```markdown
---
description: Test engineer — adds comprehensive tests, runs pytest
tools: ['search/codebase', 'search/usages', 'edit', 'read/terminalLastCommand']
---

You are a test-engineering specialist for the TaskFlow project.

When asked to write tests:
1. Read the source under test to understand behaviour
2. Read existing tests for patterns and fixtures
3. Use the `client` fixture from `tests/conftest.py` for endpoint tests
4. Cover: happy path, error cases (404/validation), edge cases (empty, max length, special chars)
5. Name tests `test_<action>_<scenario>` (e.g. `test_create_task_with_empty_title`)
6. Run `uv run pytest -v` at the end; iterate until green

Never modify the source under test. If tests fail because of a bug in the
source, call it out in your summary — do **not** silently patch production code.
```

> Need a terminal-run tool ID that's different from `read/terminalLastCommand`?
> Open **Chat → Configure Tools** to copy the current ID. Don't guess.

Switch to the new **test-writer** agent (or whatever the `description` name
resolves to) and ask:
> Add comprehensive tests for the user endpoints.

### 6.4 — Create a research-only agent
Create `.github/agents/researcher.agent.md`:
```markdown
---
description: Read-only codebase researcher — traces logic and reports findings
tools: ['search/codebase', 'search/usages', 'web/fetch']
---

You are a codebase researcher. You do not edit files, run commands, or open
PRs. You read code, trace logic, and report findings with precise
`path:line` citations.

When asked to investigate:
1. Use `search/codebase` and `search/usages` to map the territory
2. Read the relevant files end-to-end
3. Trace the flow from the entry point through to the final effect
4. Report with: Symptom • Root cause (`path:line`) • Recommendation

Always include file:line references so the reader can jump directly in.
```

Switch to **researcher** and ask:
> How does task assignment flow end-to-end from the HTTP request to the
> database?

Compare the output with what `#codebase` alone would give you — the agent
provides structure (Symptom / Root cause / Recommendation), not just facts.

### 6.5 — Custom agents vs. prompt files
Two overlapping features — here's when to pick which:

| Use a **prompt file** when… | Use a **custom agent** when… |
|------------------------------|-------------------------------|
| One-shot reusable task | Persistent working persona |
| Needs `${input:…}` placeholders | Multi-turn conversation |
| Ships in `/slash` menu | Ships in agent picker |
| Invocation: `/review src/…` | Invocation: switch agent, chat freely |

You can combine them: a **custom agent** sets the persona and tool policy; a
**prompt file** run inside it becomes a structured starting point.

### 6.6 — Interop: Claude Code agents
VS Code also reads `.claude/agents/*.md` as custom agents (a nice
cross-ecosystem bonus). If your team already maintains Claude Code agents,
Copilot will pick them up too — though the Claude-flavoured frontmatter
(`maxTurns`, `isolation: worktree`, `memory`, …) is ignored by Copilot.

## Key Takeaways
- Custom agents (was: "chat modes") live in `.github/agents/*.agent.md`
- `chat.agentFilesLocations` configures extra locations
- `tools:` uses namespaced IDs like `search/codebase`, `edit`, `web/fetch` — check **Configure Tools** for the current list
- Omit `edit` and terminal-run tools for truly read-only agents
- System prompt (the body) shapes response **structure**; `tools` shape response **abilities**
- Prompt files for one-shot tasks; custom agents for ongoing work
- Copilot also reads `.claude/agents/*.md` — zero-effort interop with Claude Code
