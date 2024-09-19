import pytest

from app.schemas import Todo


@pytest.mark.parametrize("data", [
    {"title": "Test One", "details": "Test Details", "list_id": 1, "completed": True},
    {"title": "Test Two", "details": "Test Details", "list_id": 1},
    {"title": "Test No Description", "details": "", "list_id": 1},
])
def test_create_todo(client, data):
    response = client.post("/todos/", json=data)
    assert response.status_code == 201

    created_todo = Todo(**response.json())
    assert created_todo.id is not None
    assert created_todo.created_at is not None
    assert created_todo.title == data["title"]
    assert created_todo.details == data["details"]
    assert created_todo.list_id == data["list_id"]
    assert created_todo.completed == data.get("completed", False)


def test_create_todo_invalid(client):
    response = client.post("/todos/", json={"title": "", "details": "Test Details", "list_id": 1})
    assert response.status_code == 422


@pytest.mark.parametrize("todo_index", [0, 1, 2])
def test_get_todo(client, todo_data, todo_index):
    response = client.get(f"/todos/{todo_data[todo_index].id}")
    assert response.status_code == 200

    todo = Todo(**response.json())
    assert todo.id == todo_data[todo_index].id
    assert todo.title == todo_data[todo_index].title
    assert todo.details == todo_data[todo_index].details
    assert todo.list_id == todo_data[todo_index].list_id
    assert todo.completed == todo_data[todo_index].completed
    assert todo.created_at == todo_data[todo_index].created_at


def test_get_todo_not_found(client):
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_update_todo(client, todo_data):
    data = {"title": "Updated Title", "details": "Updated Details", "list_id": 1, "completed": False}
    response = client.put(f"/todos/{todo_data[0].id}", json={"title": "Updated Title", "details": "Updated Details", "list_id": 1, "completed": False})
    assert response.status_code == 200

    updated_todo = response.json()
    assert updated_todo["title"] == data["title"]
    assert updated_todo["details"] == data["details"]
    assert updated_todo["completed"] == data["completed"]


def test_update_todo_not_found(client):
    data = {"title": "Updated Title", "details": "Updated Details", "list_id": 1, "completed": False}
    response = client.put("/todos/999", json=data)
    assert response.status_code == 404


def test_delete_todo(client, todo_data):
    response = client.delete(f"/todos/{todo_data[0].id}")
    assert response.status_code == 204


def test_delete_todo_not_found(client):
    response = client.delete("/todos/999")
    assert response.status_code == 404