# Exercise 9: Real-World Workflow — Putting It All Together

## Goal
Combine every Copilot feature you've learned into a realistic
feature-delivery workflow — from issue to merged PR — and try the async
**Copilot Coding Agent** for hands-off tasks.

## Scenario
You've been asked to add a **task search endpoint** with full-text search
by title and description.

## Workflow (local agent mode)

### Step 1 — Create a feature branch
In the Chat view (agent mode):
> Create a new branch called `feature/task-search`.

Always work on a dedicated branch — never directly on `main`.

### Step 2 — Plan with Planner mode
Switch the mode picker to **Planner** and ask:
> I need to add a search endpoint for tasks. Plan the implementation —
> what files need to change, what's the API shape, and what tests are needed?

Get a read-only plan with `path:line` citations.

### Step 3 — Scaffold with a prompt file
Switch back to **Agent**. Run:
```
/add-endpoint GET /api/v1/tasks/search — search tasks by title and description using a query parameter `q`
```

The agent will:
1. Read `src/taskflow/routers/tasks.py` for the pattern
2. Add the route + a `search_tasks` method in `database.py`
3. Write tests in `tests/test_tasks.py`
4. Run `uv run pytest`

### Step 4 — Review with Reviewer mode
Switch to **Reviewer** mode:
> Review the changes we've made in this branch.

You'll get structured **Critical / Important / Suggestions** output. Address
any Critical items.

### Step 5 — Test coverage check
Back in **Agent** mode:
```
/test-coverage src/taskflow/routers/tasks.py
```

Add any missing test cases the prompt surfaces.

### Step 6 — Commit and push
```
Commit these changes with a descriptive message, then push the branch.
```

Tip: run `/commit-message` (if you created it in Exercise 5.4) to get a
conventional-commit subject and body from the diff.

### Step 7 — Open a PR
With the GitHub MCP server connected (Exercise 7):
```
@github open a PR from feature/task-search to main. Title: "Add task search endpoint". Body: summarize the change.
```

## Workflow (Copilot Coding Agent)

Agent mode is *synchronous* — you sit in VS Code and watch it work. The
**Copilot Coding Agent** is *asynchronous* — you file an issue, assign it to
`@copilot`, and a PR appears on its own.

### Step A — File the issue
On GitHub.com, create an issue:

> **Title:** Add pagination to the task list endpoint
>
> **Body:** `GET /api/v1/tasks` should accept `limit` (default 50, max 100)
> and `offset` (default 0) query parameters. Include total count in the
> response. Add tests.

### Step B — Assign to @copilot
In the issue's right sidebar, set **Assignees** → `Copilot`. Within a
minute, a draft PR appears linked to the issue. Copilot posts its
implementation plan as the first comment.

> **Permissions:** you can also trigger or iterate the coding agent with
> `@copilot` mentions in comments — but only users with **write access** to
> the repo can do so. Read-only collaborators cannot summon the agent.

### Step C — Watch the agent work
Open the PR's **Files changed** tab. The agent commits iteratively. You'll
see test runs in the Checks tab (powered by
`.github/workflows/copilot-setup-steps.yml` — the environment bootstrap).

### Step D — Iterate via @copilot comments
Review the PR. Leave a comment:
> @copilot the pagination math is off when `offset + limit > total`. Cap it.

The agent picks up your comment, pushes a fix, and replies.

### Step E — Merge
When you're happy, approve and merge. The agent uses the same branch
protection and review rules as human contributors.

## Bonus Challenges

### Challenge A — Bug fix via `/debug`
Pick an issue and work it with `/debug`:
> /debug creating a task with a non-existent assignee should return 404,
> but it currently returns 201.

### Challenge B — Feature with edge cases
```
Add a PATCH /api/v1/tasks/{task_id}/tags endpoint that supports adding and
removing individual tags without replacing the entire list. Query params:
action=add&tag=urgent  or  action=remove&tag=urgent
```

### Challenge C — Refactoring
```
database.py is getting large. Split it into src/taskflow/db/tasks.py and
src/taskflow/db/users.py while preserving the public API. Update imports
everywhere.
```

### Challenge D — Multi-file change in one turn
```
Add a `due_date` field to tasks. Update models, database (seed data),
routers (allow filtering by overdue tasks), and tests.
```

### Challenge E — Cloud agent end-to-end
Open three small issues, assign them all to `@copilot`, and handle them as
parallel PRs. See how the async workflow scales compared to pair-programming
in agent mode.

## Key Takeaways
- Copilot features compose: instructions → prompt files → custom agents → agent mode → PR
- **Custom instructions** carry project conventions across every surface
- **Prompt files** automate repeated workflows (`/review`, `/add-endpoint`, `/test-coverage`)
- **Custom agents** swap in different personas (planner / reviewer) in seconds
- **Local agent mode** for pair-programming; **Copilot Coding Agent** for async tasks
- **MCP** bridges external systems (`@github`, databases, browsers)
- The same conventions file can serve Copilot, Claude Code, Cursor, and more — keep `.github/copilot-instructions.md`, `CLAUDE.md`, and/or `AGENTS.md` in sync
