from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session  

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