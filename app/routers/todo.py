from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.database import get_db
from app.models import ListDB, TodoDB
from app.schemas import Todo, TodoCreate

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    new_todo = TodoDB(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo


@router.get("/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> Todo:
    try:
        todo_db = db.query(TodoDB).filter(TodoDB.id == todo_id).one()
        return todo_db
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id no. {todo_id} not found.")
    

@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    list_db = db.query(ListDB).filter(ListDB.id == todo.list_id).one_or_none()

    if list_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {todo.list_id} not found.")
    
    todo_db = db.query(TodoDB).filter(TodoDB.id == todo_id)
    todo_to_update = todo_db.one_or_none()

    try:
        todo_db.update(todo.model_dump())
        db.commit()
        db.refresh(todo_to_update)
        return todo_to_update
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id no. {todo_id} not found.")

