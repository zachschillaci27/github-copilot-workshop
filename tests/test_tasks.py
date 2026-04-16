"""Tests for the task endpoints."""


def test_list_tasks(client):
    """Should return seeded tasks."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 5  # seeded data


def test_create_task(client):
    """Should create a new task."""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New test task",
            "description": "A task created in tests",
            "priority": "high",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New test task"
    assert data["status"] == "todo"
    assert data["priority"] == "high"


def test_get_task(client):
    """Should retrieve a task by ID."""
    # First create a task
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "Findable task"},
    )
    task_id = create_resp.json()["id"]

    # Then retrieve it
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Findable task"


def test_get_task_not_found(client):
    """Should return 404 for unknown task."""
    response = client.get("/api/v1/tasks/nonexistent-id")
    assert response.status_code == 404


def test_update_task(client):
    """Should update task fields."""
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "Original title"},
    )
    task_id = create_resp.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated title", "status": "in_progress"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["status"] == "in_progress"


def test_delete_task(client):
    """Should delete a task."""
    create_resp = client.post(
        "/api/v1/tasks",
        json={"title": "To be deleted"},
    )
    task_id = create_resp.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 404


def test_filter_tasks_by_status(client):
    """Should filter tasks by status."""
    response = client.get("/api/v1/tasks?status=todo")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["status"] == "todo" for t in tasks)


def test_filter_tasks_by_priority(client):
    """Should filter tasks by priority."""
    response = client.get("/api/v1/tasks?priority=critical")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["priority"] == "critical" for t in tasks)


def test_task_stats(client):
    """Should return task statistics."""
    response = client.get("/api/v1/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total"] == 5
    assert "by_status" in stats
    assert "by_priority" in stats
