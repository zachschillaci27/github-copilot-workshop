"""In-memory database for the TaskFlow API.

Uses a simple dict-based store. In a real app, you'd use SQLAlchemy or similar.
This keeps the workshop focused on GitHub Copilot features, not database setup.
"""

import uuid
from datetime import datetime, timezone

from taskflow.models import (
    Priority,
    Task,
    TaskCreate,
    TaskStatus,
    TaskUpdate,
    User,
    UserCreate,
)


class TaskDatabase:
    """Simple in-memory task store."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._users: dict[str, User] = {}
        self._seed_data()

    def _seed_data(self) -> None:
        """Add some sample data for demo purposes."""
        sample_tasks = [
            TaskCreate(
                title="Set up CI/CD pipeline",
                description="Configure GitHub Actions for testing and deployment",
                priority=Priority.HIGH,
                assignee="alice",
                tags=["devops", "infrastructure"],
            ),
            TaskCreate(
                title="Write API documentation",
                description="Document all REST endpoints with examples",
                priority=Priority.MEDIUM,
                assignee="bob",
                tags=["docs"],
            ),
            TaskCreate(
                title="Fix login timeout bug",
                description="Users are logged out after 5 min instead of 30",
                priority=Priority.CRITICAL,
                assignee="alice",
                tags=["bug", "auth"],
            ),
            TaskCreate(
                title="Add dark mode support",
                description="Implement dark mode toggle in the settings page",
                priority=Priority.LOW,
                tags=["frontend", "feature"],
            ),
            TaskCreate(
                title="Database migration script",
                description="Create migration from v1 to v2 schema",
                priority=Priority.HIGH,
                assignee="charlie",
                tags=["database", "migration"],
            ),
        ]

        sample_users = [
            UserCreate(
                username="alice", display_name="Alice Chen", email="alice@example.com"
            ),
            UserCreate(
                username="bob", display_name="Bob Smith", email="bob@example.com"
            ),
            UserCreate(
                username="charlie",
                display_name="Charlie Davis",
                email="charlie@example.com",
            ),
        ]

        for user_data in sample_users:
            self.create_user(user_data)

        for task_data in sample_tasks:
            self.create_task(task_data)

    # -------------------------------------------------------------------------
    # Task operations
    # -------------------------------------------------------------------------

    def create_task(self, data: TaskCreate) -> Task:
        now = datetime.now(timezone.utc)
        task = Task(
            id=str(uuid.uuid4()),
            title=data.title,
            description=data.description,
            priority=data.priority,
            status=TaskStatus.TODO,
            assignee=data.assignee,
            tags=data.tags,
            created_at=now,
            updated_at=now,
        )
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list_tasks(
        self,
        status: TaskStatus | None = None,
        priority: Priority | None = None,
        assignee: str | None = None,
        tag: str | None = None,
    ) -> list[Task]:
        tasks = list(self._tasks.values())

        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if priority is not None:
            tasks = [t for t in tasks if t.priority == priority]
        if assignee is not None:
            tasks = [t for t in tasks if t.assignee == assignee]
        if tag is not None:
            tasks = [t for t in tasks if tag in t.tags]

        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update_task(self, task_id: str, data: TaskUpdate) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None

        update_fields = data.model_dump(exclude_unset=True)
        updated = task.model_copy(
            update={**update_fields, "updated_at": datetime.now(timezone.utc)}
        )
        self._tasks[task_id] = updated
        return updated

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def get_task_stats(self) -> dict:
        """Return summary statistics about tasks."""
        tasks = list(self._tasks.values())
        if not tasks:
            return {"total": 0, "by_status": {}, "by_priority": {}}

        by_status = {}
        for t in tasks:
            by_status[t.status.value] = by_status.get(t.status.value, 0) + 1

        by_priority = {}
        for t in tasks:
            by_priority[t.priority.value] = by_priority.get(t.priority.value, 0) + 1

        return {
            "total": len(tasks),
            "by_status": by_status,
            "by_priority": by_priority,
        }

    # -------------------------------------------------------------------------
    # User operations
    # -------------------------------------------------------------------------

    def create_user(self, data: UserCreate) -> User:
        user = User(
            id=str(uuid.uuid4()),
            username=data.username,
            display_name=data.display_name,
            email=data.email,
            created_at=datetime.now(timezone.utc),
        )
        self._users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def list_users(self) -> list[User]:
        return sorted(self._users.values(), key=lambda u: u.created_at)

    def delete_user(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


# Global database instance
db = TaskDatabase()
