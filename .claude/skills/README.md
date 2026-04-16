# `.claude/skills/` — kept as an interop reference

This directory contains **Claude Code skills** (`SKILL.md` files with YAML
frontmatter). They are not used by GitHub Copilot, but they are kept
checked-in for two reasons:

1. **Interop demo.** The same repo is instrumented for both Copilot and
   Claude Code. Copilot gets `.github/prompts/*.prompt.md` and
   `.github/agents/*.agent.md`; Claude Code gets these skills.
2. **Side-by-side comparison.** Open one of these `SKILL.md` files next to
   its twin under `.github/prompts/` — the concepts are near-identical, only
   the frontmatter keys and discovery locations differ. Good material for a
   workshop tangent on "same idea, two ecosystems".

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
