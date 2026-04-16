# Exercise 7: MCP Servers — External Integrations

## Goal
Extend Copilot agent mode with external tools (GitHub, filesystem, databases,
browsers) via the Model Context Protocol.

> **Note:** external MCP servers require network access. If you're behind a
> corporate proxy or in a sandboxed environment, treat this exercise as a
> **conceptual walkthrough** rather than hands-on.

## Concepts

### What is MCP?
**Model Context Protocol** — an open protocol for exposing tools to AI
agents. The same MCP server can be consumed by Copilot, Claude Code, Cursor,
Windsurf, and others. GitHub, the MCP reference servers, and thousands of
community servers all speak the same wire format.

### Configuration files

| Scope | Path | Shared |
|-------|------|--------|
| Workspace | `.vscode/mcp.json` | Yes (git) |
| User | Set via Command Palette → **MCP: Open User Configuration** | No |
| Dev Container | `devcontainer.json` → `customizations.vscode.mcp.servers` | Yes |

### Transport types
- **`stdio`** — local subprocess (`npx`, `uv`, `docker run`, …)
- **`http`** — remote streaming HTTP endpoint
- **`sse`** — remote Server-Sent Events endpoint

### Enterprise policy
On Business / Enterprise plans, MCP is **disabled by default** — admins opt
in and can curate an allowed-servers list. Free / Pro users are ungoverned.

### Enablement in VS Code
`chat.mcp.access` (default `true`). Set to `false` to block all MCP servers
for this workspace.

## Tasks

### 7.1 — Inspect the MCP config
```bash
cat .vscode/mcp.json
```

Walk through:
- `inputs` — secure credential prompts (never hardcoded)
- `servers.github` — the GitHub MCP server over HTTP
- `${input:github-pat}` — references the credential defined above

### 7.2 — Start the GitHub MCP server
In the Chat view, switch to **Agent** mode. Open the **Tools** menu (wrench
icon) — you should see the GitHub server's tools (`list_issues`, `create_pr`,
etc.) as available.

When you first use one, VS Code will prompt for the `github-pat` input. Use
a fine-grained personal access token scoped to:
- `repo` → Read & Write (for issues / PRs in the workshop repo)
- `metadata` → Read

> **Security reminder:** fine-grained tokens, scoped to the minimum repos
> and permissions, are the safest credential here. Tokens live in VS Code's
> secret storage, not on disk.

### 7.3 — Use GitHub MCP tools
Ask Copilot:
> List the 5 most recently updated open issues in this repo and summarise them.

> Create a new issue titled "Add pagination to task list endpoint" with a
> description explaining why and a suggested API shape.

> Search for `TODO` comments in this repo and open an issue for the two
> most important ones.

Notice the tool calls in the Chat transcript — they look like
`github/list_issues(...)` and are subject to the same approval rules as
terminal commands.

### 7.4 — Add a filesystem MCP server (stdio example)
Edit `.vscode/mcp.json` and add:
```json
{
  "inputs": [...],
  "servers": {
    "github": { ... },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${workspaceFolder}"
      ]
    }
  }
}
```

Reload the MCP config (Command Palette → **MCP: Restart Servers**). The
server exposes file-read/write tools scoped to `${workspaceFolder}`.

> Why you'd bother: MCP filesystem tools work across surfaces (Chat,
> Coding Agent, CLI). If you're building a custom workflow that needs file
> access from the cloud agent, stdio MCP is often the right answer.

### 7.5 — Discover what's available
In Chat:
> What MCP tools do you currently have available?

Copilot lists them, grouped by server. You can also click the **Tools** icon
in the Chat view.

### 7.6 — Scoped tool access via chat modes and prompts
You can restrict any prompt file or chat mode to a specific MCP server:
```yaml
---
tools: ['github/*']        # only GitHub MCP tools
---
```
or
```yaml
---
tools: ['github/list_issues', 'github/create_issue']  # specific tools only
---
```

This is safer than giving a prompt access to the whole toolbox.

### 7.7 — Popular MCP servers to know
| Server | Transport | Purpose |
|--------|-----------|---------|
| GitHub (official) | `http` | Issues, PRs, code search (<https://api.githubcopilot.com/mcp>) |
| Filesystem | `stdio` | File access outside the workspace root |
| Playwright | `stdio` | Browser automation / end-to-end testing |
| Postgres | `sse` or `stdio` | Query a database |
| Fetch | `stdio` | Controlled HTTP fetches with allowlists |

The catalogue at <https://github.com/github/awesome-copilot> tracks vetted
servers and their security profile.

## Key Takeaways
- MCP extends agent mode with external tools, via `.vscode/mcp.json`
- Three transports: `stdio` (local), `http` (remote), `sse` (streaming)
- Credentials come from `inputs` → `${input:id}`, never hardcoded
- Restrict access per-prompt / per-chat-mode via `tools: ['server/*']`
- MCP is cross-ecosystem — the same server works with Copilot, Claude, Cursor
- Enterprise admins gate MCP at org level; check policy before shipping
