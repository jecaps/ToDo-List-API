from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  
from sqlalchemy.orm.exc import NoResultFound

from app.database import get_db
from app.models import TodoDB
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
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo_db = db.query(TodoDB).filter(TodoDB.id == todo_id).one()
        return todo_db
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id no. {todo_id} not found.")