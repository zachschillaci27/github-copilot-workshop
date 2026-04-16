# Exercise 6: Custom Chat Modes

## Goal
Build scoped AI personas (planner, reviewer, doc-writer, …) using custom
chat modes — Copilot's equivalent of Claude Code subagents.

## Concepts

### What are custom chat modes?
Markdown files that define a persistent chat persona with:
- A **system prompt** (body of the markdown)
- A scoped **tool allowlist** (`tools:` frontmatter)
- Optional **model pin** (`model:` frontmatter)
- A description shown in the mode picker

Once created, they sit alongside the built-in **Ask / Edit / Agent** modes
in the Chat's mode picker at the bottom of the input box.

### Location
```
.github/chatmodes/<name>.chatmode.md       # Workspace (shared via git)
# or user profile for personal modes
```

### Frontmatter

| Field | Purpose |
|-------|---------|
| `description` | Shown in the mode picker |
| `tools` | Array of allowed tools (built-ins, MCP server globs, extension tools) |
| `model` | (optional) Pin a specific model |

### Common tool names

| Tool | Purpose |
|------|---------|
| `codebase` | Semantic search |
| `search` | Grep-style text search |
| `usages` | Symbol usage references |
| `findTestFiles` | Test discovery |
| `problems` | Items in the VS Code Problems panel |
| `changes` | Working-tree diff |
| `fetch` | Web fetch |
| `editFiles` | File edit tool |
| `runCommands` | Terminal |
| `<mcp-server>/*` | All tools from a configured MCP server |

## Tasks

### 6.1 — Try the pre-built modes
Open the mode picker at the bottom of the Chat view. Next to **Ask / Edit /
Agent**, you'll see **Planner** and **Reviewer**.

**Switch to Planner** and ask:
> How would you refactor `database.py` to split task and user operations into
> separate modules while preserving the public API?

Notice:
- The response is a structured **plan**, not a diff
- Copilot cites `path:line` references
- It asks clarifying questions when the request is ambiguous

**Switch to Reviewer** and ask:
> Review the changes we've made so far.

You'll get structured output with **Critical / Important / Suggestions**
sections and a verdict — because the chat mode's system prompt mandates
that format.

### 6.2 — Inspect the mode files
```bash
cat .github/chatmodes/planner.chatmode.md
cat .github/chatmodes/reviewer.chatmode.md
```

Point at:
- `tools:` — no `editFiles` or `runCommands`, so these modes can't modify
  anything. That's the enforcement mechanism (not the system prompt).
- The body — it's just a Markdown system prompt.

### 6.3 — Create a test-writer mode
Create `.github/chatmodes/test-writer.chatmode.md`:
```markdown
---
description: Test engineer — adds comprehensive tests, runs pytest
tools: ['codebase', 'search', 'findTestFiles', 'editFiles', 'runCommands']
---

You are a test-engineering specialist for the TaskFlow project.

When asked to write tests:
1. Read the source under test to understand behaviour
2. Read existing tests for patterns and fixtures (use `findTestFiles`)
3. Use the `client` fixture from `tests/conftest.py` for endpoint tests
4. Cover: happy path, error cases (404/validation), edge cases (empty, max length, special chars)
5. Name tests `test_<action>_<scenario>` (e.g. `test_create_task_with_empty_title`)
6. Run `uv run pytest -v` at the end; iterate until green

Never modify the source under test. If tests fail because a bug in the
source, call it out in your summary — do **not** silently patch production code.
```

Switch to the new **Test writer** mode and ask:
> Add comprehensive tests for the user endpoints.

### 6.4 — Create a research-only mode
Create `.github/chatmodes/researcher.chatmode.md`:
```markdown
---
description: Read-only codebase researcher — traces logic and reports findings
tools: ['codebase', 'search', 'usages', 'findTestFiles', 'fetch']
---

You are a codebase researcher. You do not edit files, run commands, or open
PRs. You read code, trace logic, and report findings with precise
`path:line` citations.

When asked to investigate:
1. Use `codebase` / `search` / `usages` to map the territory
2. Read the relevant files end-to-end
3. Trace the flow from the entry point through to the final effect
4. Report with: Symptom • Root cause (`path:line`) • Recommendation

Always include file:line references so the reader can jump directly in.
```

Switch to **Researcher** and ask:
> How does task assignment flow end-to-end from the HTTP request to the
> database?

Compare the output with what `#codebase` alone would give you — the mode
provides structure (Symptom / Root cause / Recommendation), not just facts.

### 6.5 — Chat modes vs. prompt files
Two overlapping features — here's when to pick which:

| Use a **prompt file** when… | Use a **chat mode** when… |
|------------------------------|----------------------------|
| One-shot reusable task | Persistent working persona |
| Needs `${input:…}` placeholders | Multi-turn conversation |
| Ships in `/slash` menu | Ships in mode picker |
| Invocation: `/review src/…` | Invocation: switch mode, chat freely |

You can combine them: a **chat mode** sets the persona and tool policy; a
**prompt file** run inside it becomes a structured starting point.

### 6.6 — Interop: Claude Code agents
For the curious, compare:
```bash
# Copilot chat mode
cat .github/chatmodes/reviewer.chatmode.md

# Claude Code agent (conceptually equivalent)
# (removed from this repo to keep the Copilot scaffolding clean,
#  but see the awesome-copilot repo for community examples)
```

Claude Code calls them "agents" and stores them in `.claude/agents/<n>.md`
with richer frontmatter (`model`, `maxTurns`, `isolation: worktree`, …).
Copilot chat modes trade flexibility for simpler UX — same underlying idea.

## Key Takeaways
- Chat modes = persistent personas with scoped tools, in `.github/chatmodes/`
- `tools:` is the real safety boundary — omit `editFiles` / `runCommands` for read-only modes
- System prompt (the body) shapes response **structure**; tools shape response **abilities**
- Prompt files for one-shot tasks; chat modes for ongoing work
- Copilot chat modes ≈ Claude Code subagents; concept maps 1:1
