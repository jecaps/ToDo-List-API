import pytest

from app.schemas import List


@pytest.mark.parametrize("list_data", [
    {"title": "Test One", "description": "Test Description"},
    {"title": "Test Two", "description": "Test Description"},
    {"title": "Test No Description", "description": ""},
])
def test_create_list(client, list_data):
    response = client.post("/lists/", json=list_data)
    assert response.status_code == 201

    created_list = List(**response.json())
    assert created_list.id is not None
    assert created_list.title == list_data["title"]
    assert created_list.description == list_data["description"]
    assert created_list.created_at is not None
    assert created_list.updated_at is not None


def test_create_list_invalid(client):
    response = client.post("/lists/", json={"title": "","description": "Test Description"})
    assert response.status_code == 400


def test_read_lists(client, test_list):
    response = client.get("/lists/")
    assert response.status_code == 200

    list = response.json()
    assert len(list) == len(test_list)
    assert list[0]["title"] == test_list[0].title
    assert list[0]["description"] == test_list[0].description


def test_read_list(client, test_list):
    response = client.get(f"/lists/{test_list[0].id}")
    assert response.status_code == 200

    list = List(**response.json())
    assert list.id == test_list[0].id
    assert list.title == test_list[0].title
    assert list.description == test_list[0].description
    assert list.created_at == test_list[0].created_at
    assert list.updated_at == test_list[0].updated_at


def test_read_list_not_found(client):
    response = client.get("/lists/999")
    assert response.status_code == 404