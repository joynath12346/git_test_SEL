"""
Test Suite for Task Management API
Developed for Git Lab Examination (Team Mate 2: Test Implementation)
Uses pytest and FastAPI TestClient.
Verifies GET, POST, PUT, and DELETE operations, including positive and invalid/negative scenarios.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app, reset_db


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """
    Runs automatically before each test function to guarantee a clean in-memory database.
    """
    reset_db()
    yield
    reset_db()


@pytest.fixture
def client():
    """Provides a fresh FastAPI TestClient instance."""
    return TestClient(app)


# ==========================================
# Positive Scenarios (Successful Operations)
# ==========================================

def test_root_endpoint(client):
    """Verify that root endpoint is alive and returns status."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Task Management API is active" in data["message"]


def test_create_task_success(client):
    """
    Verify successful creation of a task via POST /tasks.
    Expects status code 201 Created and properly formed Task object.
    """
    payload = {
        "title": "Complete Git Lab Exam",
        "description": "Collaborate on src and test branches, setup GitHub Actions",
        "status": "pending",
        "priority": "high",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == "pending"
    assert data["priority"] == "high"


def test_get_all_tasks_success(client):
    """
    Verify GET /tasks returns all created tasks.
    """
    # Create two tasks
    client.post("/tasks", json={"title": "Task One", "status": "pending", "priority": "low"})
    client.post("/tasks", json={"title": "Task Two", "status": "completed", "priority": "high"})

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task One"
    assert tasks[1]["title"] == "Task Two"


def test_get_task_by_id_success(client):
    """
    Verify GET /tasks/{task_id} successfully retrieves a single task.
    """
    create_resp = client.post(
        "/tasks",
        json={"title": "Inspect single task", "description": "Unit test check", "priority": "medium"},
    )
    task_id = create_resp.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Inspect single task"
    assert data["priority"] == "medium"


def test_update_task_success(client):
    """
    Verify PUT /tasks/{task_id} successfully updates task fields.
    """
    create_resp = client.post(
        "/tasks",
        json={"title": "Initial Title", "description": "Old description", "status": "pending", "priority": "low"},
    )
    task_id = create_resp.json()["id"]

    update_payload = {
        "title": "Updated Title",
        "status": "completed",
        "priority": "high",
    }
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["description"] == "Old description"  # Remains unchanged
    assert data["status"] == "completed"
    assert data["priority"] == "high"


def test_delete_task_success(client):
    """
    Verify DELETE /tasks/{task_id} successfully deletes an existing task.
    """
    create_resp = client.post(
        "/tasks",
        json={"title": "Task to be deleted", "description": "Will be removed soon"},
    )
    task_id = create_resp.json()["id"]

    # Delete the task
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    assert f"Task with ID {task_id} deleted successfully" in delete_resp.json()["message"]

    # Confirm task is no longer retrievable
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


# ============================================
# Negative / Invalid Scenarios (Lab Requirement)
# ============================================

def test_get_task_not_found_invalid_scenario(client):
    """
    Invalid Scenario 1: Attempting to GET a non-existent task ID.
    Expects status code 404 NOT FOUND.
    """
    non_existent_id = 9999
    response = client.get(f"/tasks/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with ID {non_existent_id} not found"


def test_update_task_not_found_invalid_scenario(client):
    """
    Invalid Scenario 2: Attempting to PUT/update a non-existent task ID.
    Expects status code 404 NOT FOUND.
    """
    non_existent_id = 9999
    response = client.put(f"/tasks/{non_existent_id}", json={"title": "New Title"})
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with ID {non_existent_id} not found"


def test_delete_task_not_found_invalid_scenario(client):
    """
    Invalid Scenario 3: Attempting to DELETE a non-existent task ID.
    Expects status code 404 NOT FOUND.
    """
    non_existent_id = 9999
    response = client.delete(f"/tasks/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with ID {non_existent_id} not found"


def test_create_task_missing_required_title_invalid_scenario(client):
    """
    Invalid Scenario 4: Attempting to create a task without the required 'title' field.
    Expects status code 422 Unprocessable Entity (Pydantic validation failure).
    """
    invalid_payload = {
        "description": "Missing title attribute",
        "status": "pending",
    }
    response = client.post("/tasks", json=invalid_payload)
    assert response.status_code == 422


def test_create_task_invalid_status_enum_scenario(client):
    """
    Invalid Scenario 5: Attempting to create a task with an invalid status value.
    Valid options are: pending, in-progress, completed.
    Expects status code 422 Unprocessable Entity.
    """
    invalid_payload = {
        "title": "Invalid Status Task",
        "status": "not_a_valid_status",
    }
    response = client.post("/tasks", json=invalid_payload)
    assert response.status_code == 422


def test_create_task_invalid_priority_enum_scenario(client):
    """
    Invalid Scenario 6: Attempting to create a task with an invalid priority value.
    Valid options are: low, medium, high.
    Expects status code 422 Unprocessable Entity.
    """
    invalid_payload = {
        "title": "Invalid Priority Task",
        "priority": "super_urgent_emergency",
    }
    response = client.post("/tasks", json=invalid_payload)
    assert response.status_code == 422
