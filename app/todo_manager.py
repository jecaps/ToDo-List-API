from datetime import datetime
from enum import Enum

from fastapi import HTTPException, Response, status
from sqlalchemy import case
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.models import ListDB, TodoDB


class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class SortByEnum(str, Enum):
    DUE_DATE = "due_date"
    PRIORITY = "priority"
    CREATED_AT = "created_at"

class OrderEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"

class TodoManager:
    def __init__(self, db: Session):
        self.db = db

    def _apply_filters(self, query, due_date: datetime = None, priority: PriorityEnum = None):
        if due_date:
            query = query.filter(TodoDB.due_date == due_date)
        if priority:
            query = query.filter(TodoDB.priority == priority)
        return query

    def _apply_sorting(self, query, sort_by: SortByEnum, order: OrderEnum):
        if sort_by == SortByEnum.DUE_DATE:
            return query.order_by(TodoDB.due_date.desc() if order == OrderEnum.DESC else TodoDB.due_date.asc())
        elif sort_by == SortByEnum.PRIORITY:
            priority_order = case(
                {"high": 3, "medium": 2, "low": 1},
                value=TodoDB.priority
            )
            return query.order_by(priority_order.desc() if order == OrderEnum.DESC else priority_order.asc())
        else:  
            return query.order_by(TodoDB.created_at.desc() if order == OrderEnum.DESC else TodoDB.created_at.asc())

    def get_todos(
        self,
        due_date: datetime,
        priority: PriorityEnum,
        sort_by: SortByEnum,
        order: OrderEnum
    ) -> list[TodoDB]:
        query = self.db.query(TodoDB)
        query = self._apply_filters(query, due_date, priority)
        query = self._apply_sorting(query, sort_by, order)
        return query.all()

    def get_todo(self, todo_id: int)  -> TodoDB:
        try:
            todo_db = self.db.query(TodoDB).filter(TodoDB.id == todo_id).one()
            return todo_db
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id no. {todo_id} not found.")

    def create_todo(self, todo_data: dict)  -> TodoDB:
        new_todo = TodoDB(**todo_data.model_dump())
        self.db.add(new_todo)
        self.db.commit()
        self.db.refresh(new_todo)

        return new_todo

    def update_todo(self, todo_id: int, todo_data: dict)  -> TodoDB:
        list_db = self.db.query(ListDB).filter(ListDB.id == todo_data.list_id).one_or_none()

        if list_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {todo_data.list_id} not found.")

        try:
            todo_db = self.db.query(TodoDB).filter(TodoDB.id == todo_id)
            todo_to_update = todo_db.one() 
            todo_db.update(todo_data.model_dump())
            self.db.commit()
            self.db.refresh(todo_to_update)
            return todo_to_update
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id no. {todo_id} not found.")

    def delete_todo(self, todo_id: int)  -> Response:
        try:
            todo_db = self.db.query(TodoDB).filter(TodoDB.id == todo_id).one()
            self.db.delete(todo_db)
            self.db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id no. {todo_id} not found.")
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))