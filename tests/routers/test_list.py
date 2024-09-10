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