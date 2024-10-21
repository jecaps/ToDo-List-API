from datetime import datetime

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import Todo, TodoCreate
from app.todo_manager import OrderEnum, PriorityEnum, SortByEnum, TodoManager

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    return TodoManager(db).create_todo(todo)


@router.get("/")
def get_todos(
    due_date: datetime = None,
    priority: PriorityEnum = None,
    search: str = None,
    sort_by: SortByEnum = SortByEnum.CREATED_AT,
    order: OrderEnum = OrderEnum.DESC,
    completed: bool = None,
    db: Session = Depends(get_db),
)  -> list[Todo]:
    return TodoManager(db).get_todos(due_date, priority, search, sort_by, order, completed)

@router.get("/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    return TodoManager(db).get_todo(todo_id)

@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    return TodoManager(db).update_todo(todo_id, todo)
    

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> Response:
    return TodoManager(db).delete_todo(todo_id)
