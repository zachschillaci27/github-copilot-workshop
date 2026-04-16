# `.claude/skills/` — kept as an interop reference

This directory contains a single **Claude Code skill**
(`add-endpoint/SKILL.md`), kept as a side-by-side reference to its Copilot
twin at `.github/prompts/add-endpoint.prompt.md`. Claude Code reads this
skill; GitHub Copilot does not.

## Why keep it?

1. **Interop demo.** The same repo is instrumented for both Copilot and
   Claude Code. Copilot gets `.github/prompts/*.prompt.md` and
   `.github/agents/*.agent.md`; Claude Code gets this skill.
2. **Side-by-side comparison.** Open `add-endpoint/SKILL.md` next to
   `.github/prompts/add-endpoint.prompt.md` — the concepts are near-identical,
   only the frontmatter keys and discovery locations differ. Good material
   for a workshop tangent on "same idea, two ecosystems".

| Claude Code (here)       | Copilot equivalent                         |
| ------------------------ | ------------------------------------------ |
| `.claude/skills/<n>/SKILL.md` | `.github/prompts/<n>.prompt.md` (slash)    |
| `allowed-tools: …`       | `tools: [...]` in prompt-file frontmatter  |
| `$ARGUMENTS`             | `${input:name:placeholder}`                |
| `!\`cmd\`` dynamic ctx     | `#changes`, `#terminalLastCommand`, etc.   |
| `.claude/agents/*.md`    | `.github/agents/*.agent.md` (also reads `.claude/agents/*.md`) |
| `.mcp.json`              | `.vscode/mcp.json`                         |

If you're running the workshop purely on Copilot, you can safely ignore this
directory.
