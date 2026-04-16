# Exercise 1: Getting Started with GitHub Copilot

## Goal
Install Copilot in VS Code, get comfortable with inline suggestions and the
Chat view, and understand when to use Ask / Edit / Agent mode.

## Setup

Run these commands in a **regular terminal**:
```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo and install dependencies
git clone https://github.com/zachschillaci27/github-copilot-workshop.git
cd github-copilot-workshop
uv sync

# Verify everything works
uv run pytest

# Open VS Code
code .
```

In VS Code:
1. Install the **GitHub Copilot** and **GitHub Copilot Chat** extensions.
2. Sign in (status-bar Copilot icon → *Sign in*). Confirm the account has an
   active Copilot subscription.

## Tasks

### 1.1 — Inline Suggestions
Open `src/taskflow/utils.py`. At the bottom, start typing:
```python
def format_task_id(
```
Let the ghost text complete the signature, then the body. Accept with
`Tab`, dismiss with `Esc`, cycle alternatives with `Alt+]` / `Alt+[`.

### 1.2 — Chat View
Open the Chat view (`Ctrl/Cmd+Alt+I`) and ask:
- *"What does this project do?"*
- *"Show me all the API endpoints."*
- *"Explain the architecture of this project."*

Notice the **References** panel — Copilot lists the files it read, including
`.github/copilot-instructions.md`.

### 1.3 — Ask / Edit / Agent Modes
At the bottom of the Chat view there's a mode picker. Try each:

| Mode | What it does | Use when |
|------|-------------|----------|
| **Ask** | Answers questions, no edits | Exploring, explaining |
| **Edit** | Proposes a multi-file diff you approve | Focused refactor |
| **Agent** | Reads, edits, runs terminal, iterates | Multi-step tasks |

Run the same prompt in each mode and notice the difference:
> Add a `due_date: datetime | None = None` optional field to `TaskCreate`.

### 1.4 — Agent Mode + Terminal
Switch to **Agent** mode and ask:
> Add the due_date field to the Task model too, then run the tests and
> tell me if anything broke.

Watch Copilot edit multiple files, run `uv run pytest`, and iterate if tests
fail. The **Restore Checkpoint** button in the Chat header reverts everything in one
click.

### 1.5 — Attach Files and Selections
Type `#` in the chat input to browse context references:
- `#file:src/taskflow/models.py` — attach a whole file
- Select code in the editor → `#selection` picks it up automatically
- `#codebase what are the task statuses?` — semantic search the whole repo

### 1.6 — Built-in Slash Commands
In the Chat input, type `/` — you'll see built-ins plus the custom prompt
files this repo ships:
- `/explain` — explain the selection
- `/fix` — fix the error in the selection
- `/tests` — generate tests for the selection
- `/new` — scaffold a new file or workspace
- `/clear` — start a fresh chat session

Try: select `create_task` in `database.py` → `/tests`.

### 1.7 — Interrupt & Recover
While Copilot is running in Agent mode, click the **Stop** button (or press
the hotkey shown in the Chat). Then:
- Click the **Restore Checkpoint** indicator to revert its edits in one click
- Or say *"undo those changes"* and let Copilot revert them

## Key Takeaways
- Inline suggestions complete code as you type (`Tab` / `Alt+]`)
- Mode picker: Ask (read) → Edit (propose diff) → Agent (act)
- `#file`, `#selection`, `#codebase` attach context; `/slash` runs a prompt
- Agent mode pairs with **checkpoints** — one-click revert