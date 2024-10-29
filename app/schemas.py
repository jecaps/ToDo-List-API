import re
from datetime import datetime
from html import escape

from pydantic import BaseModel, Field, field_validator

from app.todo_manager import PriorityEnum


def sanitize_str(value: str | None) -> str | None:
    if value is None:
        return None
    if value == "":
        return value
    sanitized = escape(value)
    sanitized = re.sub(r'\s+', " ", sanitized)
    return sanitized.strip()

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    details: str | None = None
    completed: bool = Field(default=False)
    due_date: datetime | None = Field(default=None)
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM)

    @field_validator("title", "details")
    def sanitize_text_fields(cls, v: str | None) -> str | None:
        return sanitize_str(v)
    
    @field_validator("due_date")
    def validate_due_date(cls, v: datetime | None) -> None | datetime:
        if v is not None and v < datetime.now():
            raise ValueError("Due date cannot be in the past")
        return v

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

    @field_validator("title", "description")
    def sanitize_text_fields(cls, v: str | None) -> str | None:
        return sanitize_str(v)

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