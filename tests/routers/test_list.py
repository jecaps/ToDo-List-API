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
    response = client.get("/lists/", params={"limit": 20})
    assert response.status_code == 200

    lists = [List(**list_item) for list_item in response.json()]
    assert len(lists) == len(list_data)


@pytest.mark.parametrize("skip", [1, 2, 3, 4, 5])
def test_read_lists_skip(client, skip, list_data):
    response = client.get("/lists/", params={"skip": skip})
    assert response.status_code == 200

    lists = [List(**list_item) for list_item in response.json()]
    assert len(lists) == len(list_data) - skip


@pytest.mark.parametrize("limit", [1, 2, 3, 4, 5])
def test_read_lists_limit(client, limit, list_data):
    response = client.get("/lists/", params={"limit": limit})
    assert response.status_code == 200

    lists = [List(**list_item) for list_item in response.json()]
    assert len(lists) == limit


@pytest.mark.parametrize("sort_by", ["asc", "desc"])
def test_read_lists_sort(client, sort_by, list_data):
    response = client.get("/lists/", params={"sort_by": sort_by})
    assert response.status_code == 200

    lists = [List(**list_item) for list_item in response.json()]
    assert all(lists[i].updated_at >= lists[i + 1].updated_at for i in range(len(lists) - 1) if sort_by == "desc")
    assert all(lists[i].updated_at <= lists[i + 1].updated_at for i in range(len(lists) - 1) if sort_by == "asc")


@pytest.mark.parametrize("keyword, should_exist", [
    ("Test", True),
    ("One", True),
    ("Two", True),
    ("Three", True),
    ("Four", True),
    ("Five", True),
    ("Six", True),
    ("Seven", True),
    ("Eight", True),
    ("Nine", True),
    ("Ten", True),
    ("Eleven", False),
    ("Description", True),
])
def test_read_lists_search(client, keyword, should_exist, list_data):
    response = client.get("/lists/", params={"search": keyword})
    assert response.status_code == 200

    lists = [List(**list_item) for list_item in response.json()]
    
    if should_exist:
        assert len(lists) > 0
        assert all(keyword.lower() in list.title.lower() or 
                   (list.description and keyword.lower() in list.description.lower()) 
                   for list in lists)
    else:
        assert len(lists) == 0


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