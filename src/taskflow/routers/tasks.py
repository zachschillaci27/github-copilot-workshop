"""Task management endpoints."""

from fastapi import APIRouter, HTTPException, Query

from taskflow.database import db
from taskflow.models import (
    Priority,
    Task,
    TaskCreate,
    TaskStatus,
    TaskUpdate,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def list_tasks(
    status: TaskStatus | None = None,
    priority: Priority | None = None,
    assignee: str | None = None,
    tag: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[Task]:
    """List tasks with optional filters."""
    tasks = db.list_tasks(status=status, priority=priority, assignee=assignee, tag=tag)
    return tasks[offset : offset + limit]


@router.post("", response_model=Task, status_code=201)
def create_task(data: TaskCreate) -> Task:
    """Create a new task."""
    return db.create_task(data)


@router.get("/stats")
def get_task_stats() -> dict:
    """Get task statistics."""
    return db.get_task_stats()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    """Get a single task by ID."""
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: str, data: TaskUpdate) -> Task:
    """Update a task."""
    task = db.update_task(task_id, data)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str) -> None:
    """Delete a task."""
    if not db.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@router.post("/{task_id}/assign", response_model=Task)
def assign_task(task_id: str, assignee: str = Query(...)) -> Task:
    """Assign a task to a user."""
    user = db.get_user_by_username(assignee)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{assignee}' not found")

    task = db.update_task(task_id, TaskUpdate(assignee=assignee))
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task
