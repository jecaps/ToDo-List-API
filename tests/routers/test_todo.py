import pytest

from app.schemas import Todo


@pytest.mark.parametrize("todo_data", [
    {"title": "Test One", "details": "Test Details", "list_id": 1, "completed": True},
    {"title": "Test Two", "details": "Test Details", "list_id": 1},
    {"title": "Test No Description", "details": "", "list_id": 1},
])
def test_create_todo(client, todo_data):
    response = client.post("/todos/", json=todo_data)
    assert response.status_code == 201

    created_todo = Todo(**response.json())
    assert created_todo.id is not None
    assert created_todo.created_at is not None
    assert created_todo.title == todo_data["title"]
    assert created_todo.details == todo_data["details"]
    assert created_todo.list_id == todo_data["list_id"]
    assert created_todo.completed == todo_data.get("completed", False)


def test_create_todo_invalid(client):
    response = client.post("/todos/", json={"title": "", "details": "Test Details", "list_id": 1})
    assert response.status_code == 422


def test_get_todo(client, test_todo):
    response = client.get(f"/todos/{test_todo[0].id}")
    assert response.status_code == 200

    todo = Todo(**response.json())
    assert todo.id == test_todo[0].id
    assert todo.title == test_todo[0].title
    assert todo.details == test_todo[0].details
    assert todo.list_id == test_todo[0].list_id
    assert todo.completed == test_todo[0].completed
    assert todo.created_at == test_todo[0].created_at


def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404