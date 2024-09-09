from datetime import datetime
from typing import List as PyList
from typing import Optional

from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    details: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    list_id: int
    class Config:
        orm_mode = True

class ListBase(BaseModel):
    title: str 
    description: Optional[str] = None

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    created_at: datetime
    updated_at: datetime
    todos: PyList[Todo] = []
    class Config:
        orm_mode = True

class ListWithoutTodos(ListBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True