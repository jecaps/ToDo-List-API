import pytest

from app.schemas import List


@pytest.mark.parametrize("data", [
    {"title": "Test One", "description": "Test Description"},
    {"title": "Test Two", "description": "Test Description"},
    {"title": "Test No Description", "description": ""},
])
def test_create_list(client, data):
    response = client.post("/lists/", json=data)
    assert response.status_code == 201

    created_list = List(**response.json())
    assert created_list.id is not None
    assert created_list.title == data["title"]
    assert created_list.description == data["description"]
    assert created_list.created_at is not None
    assert created_list.updated_at is not None


def test_create_list_invalid(client):
    response = client.post("/lists/", json={"title": "","description": "Test Description"})
    assert response.status_code == 422


def test_read_lists(client, list_data):
    response = client.get("/lists/")
    assert response.status_code == 200

    list = response.json()
    assert len(list) == len(list_data)
    assert list[0]["title"] == list_data[0].title
    assert list[0]["description"] == list_data[0].description


def test_read_list(client, list_data):
    response = client.get(f"/lists/{list_data[0].id}")
    assert response.status_code == 200

    list = List(**response.json())
    assert list.id == list_data[0].id
    assert list.title == list_data[0].title
    assert list.description == list_data[0].description
    assert list.created_at == list_data[0].created_at
    assert list.updated_at == list_data[0].updated_at


def test_read_list_not_found(client):
    response = client.get("/lists/999")
    assert response.status_code == 404


def test_update_list(client, list_data):
    response = client.put(f"/lists/{list_data[0].id}", json={"title": "Updated Title", "description": "Updated Description"})
    assert response.status_code == 200

    updated_list = response.json()
    assert updated_list["title"] == list_data[0].title
    assert updated_list["description"] == list_data[0].description
    

def test_update_list_not_found(client):
    response = client.put("/lists/999", json={"title": "Updated Title", "description": "Updated Description"})
    assert response.status_code == 404


def test_update_list_invalid(client, list_data):
    response = client.put(f"/lists/{list_data[0].id}", json={"title": "","description": "Updated Description"})
    assert response.status_code == 422
    

def test_delete_list(client, list_data):
    response = client.delete(f"/lists/{list_data[2].id}")
    assert response.status_code == 204

    response = client.delete(f"/lists/{list_data[2].id}")
    assert response.status_code == 404


def test_delete_list_not_found(client):
    response = client.delete("/lists/999")
    assert response.status_code == 404