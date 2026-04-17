# Exercise 7: Agent Hooks

## Goal
Automate and enforce behaviour around agent sessions with **hooks** — shell
commands that run at defined lifecycle events (before/after a tool call,
session start, session stop, …).

> **Preview feature.** Agent hooks in VS Code are currently in Preview. The
> config format and behaviour may still change. Enterprise admins can disable
> hooks org-wide — check policy before relying on them in a shared repo.

## Concepts

### Why hooks?
Instructions and custom agents *guide* the model; hooks *guarantee*
deterministic behaviour because they're plain shell commands the extension
executes itself. Common uses:

- **Security policy**: block `rm -rf`, `DROP TABLE`, force-push, … before
  the tool call fires.
- **Code quality**: run `ruff format` / `ruff check` automatically after
  every file edit.
- **Audit trail**: log every tool invocation with timestamp + session ID.
- **Context injection**: add `git branch`, `uv --version`, or project
  metadata at session start so the agent starts informed.
- **Approvals**: auto-allow safe operations, force `ask` on sensitive ones.

### Lifecycle events

| Event | Fires when… | Typical use |
|-------|-------------|-------------|
| `SessionStart` | A new chat session begins | Inject project context |
| `UserPromptSubmit` | User sends a message | Audit prompts, inject system context |
| `PreToolUse` | Before any tool call | Block, rewrite, or require approval |
| `PostToolUse` | After a tool call completes | Format, lint, log |
| `PreCompact` | Before context compaction | Export state before truncation |
| `SubagentStart` / `SubagentStop` | A sub-agent is spawned / completes | Track nested agent use |
| `Stop` | The agent session ends | Summary, cleanup, notifications |

### Configuration locations

| Scope | Path |
|-------|------|
| Workspace (Copilot) | `.github/hooks/*.json` |
| Workspace (Claude format) | `.claude/settings.json`, `.claude/settings.local.json` |
| User | `~/.copilot/hooks`, `~/.claude/settings.json` |
| Custom agent | `hooks:` field in `.agent.md` frontmatter |

Configurable via `chat.hookFilesLocations`. Workspace hooks override user
hooks for the same event.

### Hook config shape

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "./scripts/format.sh",
        "windows": "powershell -File scripts\\format.ps1",
        "timeout": 30,
        "env": { "LOG_LEVEL": "info" }
      }
    ]
  }
}
```

Hooks receive a JSON payload on **stdin** and return JSON on **stdout**.
Exit code drives the outcome:

| Exit code | Meaning |
|-----------|---------|
| `0` | Success — stdout parsed as JSON |
| `2` | Blocking error — stderr shown to the model |
| other | Non-blocking warning — shown to the user |

## Tasks

### 10.1 — A first `PostToolUse` hook: auto-format Python
Create [.github/hooks/format.json](../.github/hooks/format.json):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "./scripts/format-python.sh",
        "timeout": 15
      }
    ]
  }
}
```

Create [scripts/format-python.sh](../scripts/format-python.sh) (remember
`chmod +x`):
```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE=$(echo "$INPUT" | jq -r '.tool_input.filePath // .tool_input.path // empty')

if [[ "$TOOL_NAME" == "create_file" || "$TOOL_NAME" == "replace_string_in_file" ]]; then
  if [[ "$FILE" == *.py && -f "$FILE" ]]; then
    uv run ruff format "$FILE" 2>/dev/null
  fi
fi

echo '{"continue":true}'
```

Ask Copilot to add a small helper to `src/taskflow/utils.py`. After the edit
completes, open **Output → GitHub Copilot Chat Hooks** to see the hook fire.

> **Tool name tip.** Copilot uses `create_file` and `replace_string_in_file`;
> Claude Code uses `Write` and `Edit`. If you copy a hook between the two,
> match your `tool_name` checks accordingly.

### 10.2 — A `PreToolUse` hook: block dangerous commands
Create [.github/hooks/security.json](../.github/hooks/security.json):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/block-dangerous.sh",
        "timeout": 5
      }
    ]
  }
}
```

Create [scripts/block-dangerous.sh](../scripts/block-dangerous.sh):
```bash
#!/bin/bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [[ "$TOOL_NAME" == "run_in_terminal" ]]; then
  if echo "$COMMAND" | grep -qiE '(rm\s+-rf\s+/|drop\s+table|git\s+push\s+.*--force|:\(\)\{)'; then
    jq -n --arg cmd "$COMMAND" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("Destructive command blocked by security hook: " + $cmd)
      }
    }'
    exit 0
  fi
fi

echo '{"continue":true}'
```

Test it by asking Copilot:
> Run `rm -rf /tmp/foo` in the terminal.

You should see the tool call blocked with the reason from the hook.

> **Permission decision priority.** When multiple hooks run for the same
> tool, the most restrictive wins: `deny` > `ask` > `allow`. One hook
> saying `deny` will override any number of `allow`s.

### 10.3 — `SessionStart` context injection
Create [.github/hooks/context.json](../.github/hooks/context.json):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "./scripts/inject-context.sh"
      }
    ]
  }
}
```

Create [scripts/inject-context.sh](../scripts/inject-context.sh):
```bash
#!/bin/bash
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
PY=$(uv run python --version 2>/dev/null || echo "unknown")
TESTS=$(find tests -name 'test_*.py' 2>/dev/null | wc -l | tr -d ' ')

jq -n \
  --arg branch "$BRANCH" \
  --arg py "$PY" \
  --arg tests "$TESTS" \
  '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: ("Branch: " + $branch + " | " + $py + " | " + $tests + " test files")
    }
  }'
```

Start a new chat session and ask:
> What environment am I working in?

Copilot should cite the injected branch / Python version / test-file count
without having to run any tools.

### 10.4 — Audit trail with `PreToolUse`
Create [.github/hooks/audit.json](../.github/hooks/audit.json):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/audit.sh",
        "env": { "AUDIT_LOG": ".github/hooks/audit.log" }
      }
    ]
  }
}
```

Create [scripts/audit.sh](../scripts/audit.sh):
```bash
#!/bin/bash
INPUT=$(cat)
TS=$(echo "$INPUT" | jq -r '.timestamp')
SID=$(echo "$INPUT" | jq -r '.sessionId')
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

echo "[$TS] session=$SID tool=$TOOL" >> "${AUDIT_LOG:-audit.log}"
echo '{"continue":true}'
```

Add `.github/hooks/audit.log` to `.gitignore`. Run a couple of prompts, then
`cat .github/hooks/audit.log` — every tool invocation is logged.

### 10.5 — Agent-scoped hooks
Hooks can also live inside a custom agent's frontmatter (Exercise 6). They
only fire while *that* agent is active.

Enable with `chat.useCustomAgentHooks: true` in VS Code settings, then add a
hooks block to an agent file:

```markdown
---
description: Strict formatter — auto-formats Python after every edit
tools: ['search/codebase', 'edit', 'read/terminalLastCommand']
hooks:
  PostToolUse:
    - type: command
      command: "./scripts/format-python.sh"
---

You are a code editor for TaskFlow. After any change, formatting runs
automatically via the PostToolUse hook.
```

Switch to that agent and make an edit — the format hook fires. Switch back
to the default agent and make an equivalent edit — no hook runs.

### 10.6 — Manage hooks via the UI
Open the Chat view and type `/hooks`, or run **Chat: Configure Hooks** from
the Command Palette.

The UI lets you:
- Browse every registered hook per event type
- Jump straight into the JSON file with the cursor on the `command` field
- Create a new hook file scaffolded for the chosen event

For AI-assisted generation, type `/create-hook` in chat and describe what
you want, e.g.:
> Create a hook that runs `uv run pytest -x` after any edit to a file under `tests/`.

Copilot produces the JSON config + the shell script.

### 10.7 — Interop: Claude Code `settings.json`
Copilot reads `.claude/settings.json` by default. Add hooks there for
cross-tool reuse:
```json
{
  "hooks": {
    "PostToolUse": [
      { "type": "command", "command": "./scripts/format-python.sh" }
    ]
  }
}
```

Caveats when porting Claude hooks to Copilot:
- **Property names**: Claude uses `snake_case` (`tool_input.file_path`),
  Copilot uses `camelCase` (`tool_input.filePath`). Update your `jq` paths.
- **Tool names**: Claude `Edit` / `Write` → Copilot
  `replace_string_in_file` / `create_file`.
- **Matchers ignored**: Claude's `"matcher": "Edit|Write"` is parsed but not
  enforced by VS Code — the hook runs on *every* tool of that event type.

If you want Copilot to stop reading Claude hooks entirely:
```json
"chat.hookFilesLocations": {
  ".claude/settings.json": false,
  ".claude/settings.local.json": false,
  "~/.claude/settings.json": false
}
```

### 10.8 — Diagnose a broken hook
Intentionally break a hook — e.g. remove `chmod +x` from
`scripts/audit.sh`, or return invalid JSON. Trigger a tool call, then:

1. **Output panel → GitHub Copilot Chat Hooks** — see stderr and parse
   errors.
2. **View → Logs** → search for `Load Hooks` — confirms which files loaded
   and from where.

Common failure modes:
- Permission denied → `chmod +x` the script.
- `JSON parse error` → always emit valid JSON; use `jq -n` to build it.
- Timed out → raise `timeout` (default 30 s) or make the script faster.
- Hook silently ignored → the filename must end in `.json` and live under
  a location listed in `chat.hookFilesLocations`.

## Safety

If an agent has `edit` access to your hook scripts, it can **modify the code
that gates its own behaviour**. Two guardrails:

1. Set `chat.tools.edits.autoApprove` to require manual approval for edits
   under `scripts/` and `.github/hooks/`.
2. Review hooks pulled in from shared repos before trusting them — they run
   with the same permissions as VS Code itself.

Never hardcode secrets in hook scripts; use `env:` in the config or a
credential helper.

## Key Takeaways
- Hooks are deterministic shell commands at lifecycle events — not advice to
  the model.
- Eight events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
  `PostToolUse`, `PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`.
- Config lives in `.github/hooks/*.json`, `.claude/settings.json`, or an
  agent's frontmatter; `chat.hookFilesLocations` controls discovery.
- Stdin is JSON in, stdout is JSON out; exit code `2` blocks, `0` succeeds.
- `PreToolUse.hookSpecificOutput.permissionDecision` is the fine-grained
  control (`allow` / `deny` / `ask`); `continue: false` stops the whole
  session.
- Most restrictive decision wins across overlapping hooks.
- Interop with Claude Code via `.claude/settings.json`, but watch out for
  snake_case vs camelCase tool inputs and different tool names.
