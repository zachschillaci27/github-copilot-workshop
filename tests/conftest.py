"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from taskflow.database import TaskDatabase, db
from taskflow.main import app


@pytest.fixture
def client():
    """Create a test client with a fresh database."""
    # Reset global db state for test isolation
    db.__init__()
    return TestClient(app)


@pytest.fixture
def empty_db():
    """Create a completely empty database (no seed data)."""
    fresh = TaskDatabase.__new__(TaskDatabase)
    fresh._tasks = {}
    fresh._users = {}
    return fresh
