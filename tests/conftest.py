import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import ListDB, TodoDB
from app.schemas import Todo

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def list_data(session):
    data = [
        {"title": "Test One", "description": "Test Description One"},
        {"title": "Test Two", "description": "Test Description Two"},
        {"title": "Test 3", "description": ""},
    ]

    def create_list_model(list):
        return ListDB(**list)
    
    lists_map = map(create_list_model, data)
    lists = list(lists_map)

    session.add_all(lists)
    session.commit()

    new_lists = session.query(ListDB).all()
    return new_lists


@pytest.fixture()
def todo_data(session, list_data):
    data = [
        {"title": "Test One", "details": "Test Details", "list_id": list_data[0].id, "completed": True},
        {"title": "Test Two", "details": "Test Details", "list_id": list_data[1].id},
        {"title": "Test No Description", "details": "", "list_id": list_data[2].id},
    ]

    def create_todo_model(todo):
        return TodoDB(**todo)
    
    todos_map = map(create_todo_model, data)
    todos = list(todos_map)

    session.add_all(todos)
    session.commit()

    new_todos = session.query(TodoDB).all()
    return [Todo.model_validate(todo) for todo in new_todos]
