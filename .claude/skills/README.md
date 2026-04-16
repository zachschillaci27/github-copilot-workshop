# `.claude/skills/` — kept as an interop reference

This directory contains a single **Claude Code skill**
(`add-endpoint/SKILL.md`), kept as a side-by-side reference to its Copilot
twin at `.github/prompts/add-endpoint.prompt.md`. Claude Code reads this
skill; GitHub Copilot does not.

> **Conceptual caveat.** A Copilot **prompt file** is *user-invoked* via a
> `/slash` command. A Claude Code **skill** is *model-invoked* — Claude
> auto-loads it when the user's request matches the skill's `description`.
> The closest user-invoked Claude analog is a slash command in
> `.claude/commands/`. We use a skill here anyway because it's the
> higher-leverage Claude Code primitive and the body of the file ends up
> almost identical to the prompt file.

## Why keep it?

1. **Interop demo.** The same repo is instrumented for both Copilot and
   Claude Code. Copilot gets `.github/prompts/*.prompt.md` and
   `.github/agents/*.agent.md`; Claude Code gets this skill.
2. **Side-by-side comparison.** Open `add-endpoint/SKILL.md` next to
   `.github/prompts/add-endpoint.prompt.md` — the bodies are near-identical;
   the frontmatter, invocation model, and discovery location differ. Good
   material for a workshop tangent on "same idea, two ecosystems".

| Claude Code (here)            | Copilot equivalent                                              |
| ----------------------------- | --------------------------------------------------------------- |
| `.claude/skills/<n>/SKILL.md` | `.github/prompts/<n>.prompt.md`                                 |
| Auto-loaded by `description`  | User-invoked via `/<n>`                                         |
| `name`, `description` only    | `agent`, `description`, optional `tools`, `model`               |
| Body asks for natural-language args | `${input:name:placeholder}` for structured args           |
| `.claude/agents/*.md`         | `.github/agents/*.agent.md` (Copilot also reads `.claude/agents/*.md`) |
| `.mcp.json`                   | `.vscode/mcp.json`                                              |

If you're running the workshop purely on Copilot, you can safely ignore this
directory.
