from datetime import datetime

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


def test_get_todos(client, todo_data):
    response = client.get("/todos/")
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    for i, todo in enumerate(todos):
        assert todo.id == todo_data[i].id
        assert todo.title == todo_data[i].title
        assert todo.details == todo_data[i].details
        assert todo.list_id == todo_data[i].list_id
        assert todo.completed == todo_data[i].completed
        assert todo.created_at == todo_data[i].created_at


@pytest.mark.parametrize("priority_level", ["high", "medium", "low"])
def test_get_todos_filter_by_priority(client, priority_level):
    response = client.get("/todos/", params={"priority": priority_level})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]

    for todo in todos:
        assert todo.priority == priority_level


def test_get_todos_filter_by_due_date(client):
    due_date = datetime(2024, 10, 21, 0, 0, 0)
    response = client.get("/todos", params={"due_date": due_date})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]

    for todo in todos:
        assert todo.due_date == due_date


def test_get_todos_sort_by_due_date_asc(client, todo_data):
    response = client.get("/todos/", params={"sort_by": "due_date", "order": "asc"})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    for i in range(1, len(todos)):
        current_date = todos[i].due_date
        previous_date = todos[i - 1].due_date
        
        if current_date is None and previous_date is None:
            continue
            
        assert (previous_date is None or current_date is not None and current_date >= previous_date)


def test_get_todos_sort_by_due_date_desc(client, todo_data):
    response = client.get("/todos/", params={"sort_by": "due_date"})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    for i in range(1, len(todos)):
        current_date = todos[i].due_date
        previous_date = todos[i - 1].due_date
        
        if current_date is None and previous_date is None:
            continue
            
        assert (current_date is None or previous_date is not None and current_date <= previous_date)


def test_get_todos_sort_by_priority_asc(client, todo_data):
    response = client.get("/todos/", params={"sort_by": "priority", "order": "asc"})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    priority_order = {"high": 3, "medium": 2, "low": 1}

    for i in range(1, len(todos)):
        current_priority = priority_order[todos[i].priority]
        previous_priority = priority_order[todos[i - 1].priority]
        assert current_priority >= previous_priority


def test_get_todos_sort_by_priority_desc(client, todo_data):
    response = client.get("/todos/", params={"sort_by": "priority"})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    priority_order = {"high": 3, "medium": 2, "low": 1}

    for i in range(1, len(todos)):
        current_priority = priority_order[todos[i].priority]
        previous_priority = priority_order[todos[i - 1].priority]
        assert current_priority <= previous_priority


def test_get_todos_sort_by_created_at_asc(client, todo_data):
    response = client.get("/todos/", params={"sort_by": "created_at", "order": "asc"})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    for i in range(1, len(todos)):
        assert todos[i].created_at >= todos[i - 1].created_at

        
def test_get_todos_sort_by_created_at_desc(client, todo_data):
    response = client.get("/todos/", params={"sort_by": "created_at", "order": "desc"})
    assert response.status_code == 200

    todos = [Todo(**todo) for todo in response.json()]
    assert len(todos) == len(todo_data)

    for i in range(1, len(todos)):
        assert todos[i].created_at <= todos[i - 1].created_at


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