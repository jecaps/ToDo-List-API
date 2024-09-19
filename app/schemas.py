from datetime import datetime

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    details: str | None = None
    completed: bool = False

class TodoCreate(TodoBase):
    list_id: int

class Todo(TodoBase):
    id: int
    created_at: datetime
    list_id: int
    class Config:
        from_attributes = True

class ListBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    created_at: datetime
    updated_at: datetime
    todos: list[Todo] = []
    class Config:
        from_attributes = True

class ListWithoutTodos(ListBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True