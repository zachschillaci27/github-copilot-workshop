# Exercise 3: Settings & Permissions

## Goal
Configure Copilot's behaviour in VS Code — enablement, auto-approve rules,
model selection, and content exclusion.

## Concepts

### Settings scopes
| Scope | Path | Shared |
|-------|------|--------|
| Workspace | `.vscode/settings.json` | Yes (git) |
| User | VS Code user settings (JSON) | No |
| Org/Enterprise | GitHub admin console | Yes (policy) |

### Key Copilot settings

| Setting | Purpose |
|---------|---------|
| `github.copilot.enable` | Per-language toggle for inline suggestions |
| `chat.agent.enabled` | Enable agent mode |
| `chat.agent.maxRequests` | Cap on agent tool calls per turn (default 25) |
| `chat.checkpoints.enabled` | Revertable agent edits |
| `chat.tools.terminal.enableAutoApprove` | Master switch for terminal allowlist |
| `chat.tools.terminal.autoApprove` | Allow/deny map for terminal commands (keys: literal command or `/^regex/flags`) |
| `chat.tools.edits.autoApprove` | Which edit tools bypass approval |
| `github.copilot.chat.codesearch.enabled` | Enable automatic `#codebase` discovery |
| `chat.promptFilesLocations` | Extra locations to search for prompt files |
| `chat.instructionsFilesLocations` | Extra locations for instructions |
| `chat.agentFilesLocations` | Extra locations for custom agents (formerly "chat modes") |
| `chat.mcp.access` | Enable MCP server usage |

## Tasks

### 3.1 — Inspect current settings
```bash
cat .vscode/settings.json
```
Note the allowlist under `chat.tools.terminal.autoApprove` and the denylist
entries (`rm`, `sudo`, `curl`).

### 3.2 — Experience auto-approve in action
In Chat (Agent mode), ask:
1. *"Run the tests"* → auto-approved (`uv run pytest` is in the allowlist)
2. *"Run `uv run ruff format src/`"* → auto-approved (matches `uv run ruff`)
3. *"Run `sudo apt update`"* → blocked (denylist)
4. *"Run `git log --oneline -5`"* → auto-approved (regex pattern match)

### 3.3 — Tighten the allowlist
Temporarily edit `.vscode/settings.json` — replace the allowlist with
read-only commands only:
```json
"chat.tools.terminal.autoApprove": {
  "/^git (status|diff|log|branch|show)\\b/": true,
  "ls": true,
  "cat": true,
  "rm": false,
  "sudo": false
}
```

> **Key format.** A key that starts and ends with `/` is treated as a
> JavaScript-style regex (with optional trailing flags like `i`). Any other
> key is matched as a literal command prefix. Because the key is a JSON
> string, you still need to JSON-escape backslashes (note the `\\b` above).
Now ask Copilot to run the tests. It will prompt for approval on every run —
useful on a production machine or unfamiliar codebase.

Restore the original settings when done:
```bash
git checkout .vscode/settings.json
```

### 3.4 — Per-language enablement
Open VS Code user settings (`Ctrl/Cmd+,`, click the `{}` icon for JSON).
Edit `github.copilot.enable`:
```json
"github.copilot.enable": {
  "*": true,
  "plaintext": false,
  "markdown": true,
  "scminput": false,
  "yaml": false
}
```
`scminput: false` keeps Copilot out of commit message drafts. `yaml: false`
is handy if your YAML context (Helm, k8s) produces noisy suggestions.

### 3.5 — Model picker
Click the **model name** at the bottom of the Chat input. You'll see tiers
like:
- Fast / general (default)
- Deep reasoning (for multi-step or ambiguous tasks)
- Lightweight (for fast, focused edits)

> Availability depends on your plan. The model picker is available on
> Copilot Pro, Pro+, Business, and Enterprise — Free does not get it.

Re-run the same prompt with two different models and compare responses:
> Refactor `database.py` to split task operations and user operations into
> separate modules while preserving the public API.

### 3.6 — Content exclusion (Business/Enterprise)
Org and enterprise admins can mark paths or repos as excluded — Copilot
won't send those files as context, won't offer inline suggestions in them,
and won't use them to inform suggestions elsewhere.

For this workshop, view the concept:
- **GitHub.com** → Org/Enterprise settings → **Copilot** → **Content exclusion**
- You can exclude per-repo via glob patterns (e.g. `secrets/**`)

Caveat: **indirect** context can still leak (function signatures referenced
from other files, build configs). Exclusion is a coarse filter, not an
information-theoretic guarantee.

### 3.7 — `chat.tools.global.autoApprove` — don't touch this
Setting this to `true` disables **all** approval gates across all tools. It
exists for power users; it's a bad idea for most teams. Open the setting,
read the hover, and close it.

## Key Takeaways
- `.vscode/settings.json` = team-shared workspace settings; VS Code user
  settings = personal
- Terminal auto-approve is the closest Copilot analog to Claude Code's
  allow/deny permission lists
- Per-language enablement keeps Copilot out of sensitive file types
- Model picker lets you trade speed vs. reasoning depth per turn
- Content exclusion is an enterprise-only feature and is indirect only
