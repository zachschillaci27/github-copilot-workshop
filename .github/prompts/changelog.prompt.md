---
mode: ask
description: Generate a changelog entry from recent commits
---

# Generate Changelog

Produce a user-facing changelog entry covering the recent changes on this branch.

Use `#changes` to inspect the working-tree diff and the last few commits via
the terminal (`git log --oneline -10`).

Group entries under the standard Keep a Changelog headings:

- **Added** — new features
- **Changed** — updates to existing behaviour
- **Fixed** — bug fixes
- **Removed** — removed features

Keep entries short, user-facing, and free of implementation jargon.
