"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from taskflow.models import Priority, TaskCreate, TaskStatus, UserCreate


def test_task_create_defaults():
    """Should set correct defaults."""
    task = TaskCreate(title="Test task")
    assert task.priority == Priority.MEDIUM
    assert task.description == ""
    assert task.tags == []
    assert task.assignee is None


def test_task_create_validation():
    """Should reject invalid data."""
    with pytest.raises(ValidationError):
        TaskCreate(title="")  # too short

    with pytest.raises(ValidationError):
        TaskCreate(title="x" * 201)  # too long


def test_user_create_username_validation():
    """Should validate username format."""
    # Valid usernames
    UserCreate(username="alice", display_name="Alice", email="a@b.com")
    UserCreate(username="bob-123", display_name="Bob", email="b@c.com")
    UserCreate(username="charlie_x", display_name="Charlie", email="c@d.com")

    # Invalid usernames
    with pytest.raises(ValidationError):
        UserCreate(username="ab", display_name="Too Short", email="x@y.com")

    with pytest.raises(ValidationError):
        UserCreate(username="has spaces", display_name="Bad", email="x@y.com")


def test_priority_values():
    """Should have correct priority values."""
    assert Priority.LOW == "low"
    assert Priority.MEDIUM == "medium"
    assert Priority.HIGH == "high"
    assert Priority.CRITICAL == "critical"


def test_task_status_values():
    """Should have correct status values."""
    assert TaskStatus.TODO == "todo"
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskStatus.DONE == "done"
    assert TaskStatus.ARCHIVED == "archived"
