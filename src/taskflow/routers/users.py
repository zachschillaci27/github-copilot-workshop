"""User management endpoints."""

from fastapi import APIRouter, HTTPException

from taskflow.database import db
from taskflow.models import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
def list_users() -> list[User]:
    """List all users."""
    return db.list_users()


@router.post("", response_model=User, status_code=201)
def create_user(data: UserCreate) -> User:
    """Create a new user."""
    existing = db.get_user_by_username(data.username)
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Username '{data.username}' already taken",
        )
    return db.create_user(data)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str) -> User:
    """Get a user by ID."""
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str) -> None:
    """Delete a user."""
    if not db.delete_user(user_id):
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.get("/{user_id}/tasks")
def get_user_tasks(user_id: str) -> dict:
    """Get all tasks assigned to a user."""
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    tasks = db.list_tasks(assignee=user.username)
    return {
        "user": user,
        "tasks": tasks,
        "total": len(tasks),
    }
