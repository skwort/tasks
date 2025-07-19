import os
import pytest
from tasks import create_app
import http


@pytest.fixture()
def app():
    config = {
        "DATABASE_URI": "sqlite:///pytest.db"
    }
    app = create_app(config)

    yield app

    os.remove("pytest.db")


@pytest.fixture()
def client(app):
    return app.test_client()


def test_api_tasks_get_ok(client):
    """
    Test the GET /api/tasks endpoint.
    """
    # Initially no tasks
    response = client.get("/api/tasks")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json == []

    # Add a task
    task = {
        "id": 12345,
        "category": "unsched",
        "category_rank": 0,
        "title": "Test Task",
        "body": "This is some test body",
    }
    client.post("/api/tasks", json=task)

    # Fetch tasks again
    response = client.get("/api/tasks")
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json) == 1
    assert response.json[0] == task


def test_api_tasks_post_ok(client):
    task = {
        "id": 12345,
        "category": "unsched",
        "category_rank": 0,
        "title": "Test Task",
        "body": "This is some test body",
    }

    response = client.post("/api/tasks", json=task)
    assert response.status_code == http.HTTPStatus.CREATED


def test_api_tasks_post_conflict(client):
    """
    Test POST fails when id already exists (task id is unique).
    """
    task = {
        "id": 12345,
        "category": "unsched",
        "category_rank": 0,
        "title": "Test Task",
        "body": "This is some test body",
    }

    response = client.post("/api/tasks", json=task)
    assert response.status_code == http.HTTPStatus.CREATED

    # POST a task with the same id
    response = client.post("/api/tasks", json=task)
    assert response.status_code == http.HTTPStatus.CONFLICT


def test_api_tasks_patch_ok(client):
    task = {
        "id": 12345,
        "category": "unsched",
        "category_rank": 0,
        "title": "Test Task",
        "body": "This is some test body",
    }

    response = client.post("/api/tasks", json=task)
    assert response.status_code == http.HTTPStatus.CREATED

    # Update mutable fields
    update = {
        "id": 12345,
        "category": "must_do",
        "category_rank": 0,
        "title": "Updated Task",
        "body": "This is the updated test body",
    }
    response = client.patch("/api/tasks", json=update)
    assert response.status_code == http.HTTPStatus.OK

    # Check fields were patched
    response = client.get("/api/tasks")
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json) == 1
    assert response.json[0] == update


def test_api_tasks_patch_not_found(client):
    """
    Test PATCH /api/tasks when the task is not found.
    """
    task = {
        "id": 12345,
        "category": "unsched",
        "category_rank": 0,
        "title": "Test Task",
        "body": "This is some test body",
    }
    response = client.patch("/api/tasks", json=task)
    assert response.status_code == http.HTTPStatus.NOT_FOUND


def test_api_tasks_delete_ok(client):
    """
    Test the DELETE /api/tasks endpoint.
    """
    # Add a task
    task = {
        "id": 12345,
        "category": "unsched",
        "category_rank": 0,
        "title": "Test Task",
        "body": "This is some test body",
    }
    client.post("/api/tasks", json=task)

    # Ensure the task is added
    response = client.get("/api/tasks")
    assert len(response.json) == 1

    # Delete the task
    response = client.delete("/api/tasks?id=12345")
    assert response.status_code == http.HTTPStatus.OK

    # Ensure the task is deleted
    response = client.get("/api/tasks")
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json) == 0


def test_api_tasks_delete_not_found(client):
    """
    Test DELETE /api/tasks when the task is not found.
    """
    response = client.delete("/api/tasks?id=99999")
    assert response.status_code == http.HTTPStatus.NOT_FOUND
