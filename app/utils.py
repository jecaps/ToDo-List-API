import enum
from datetime import datetime

from sqlalchemy import case

from app.models import TodoDB


class PriorityEnum(str, enum.Enum):
    high = "high"
    medium = "medium"
    low = "low"

class SortByEnum(str, enum.Enum):
    due_date = "due_date"
    priority = "priority"

class OrderEnum(str, enum.Enum):
    asc = "asc"
    desc = "desc"

def apply_filters(query, due_date: datetime, priority: PriorityEnum):
    if due_date:
        query = query.filter(TodoDB.due_date == due_date)
    if priority:
        query = query.filter(TodoDB.priority == priority)
    return query

def apply_sorting(query, sort_by: SortByEnum, order: OrderEnum):
    if sort_by == SortByEnum.due_date:
        return query.order_by(TodoDB.due_date.desc() if order == OrderEnum.desc else TodoDB.due_date.asc())
    elif sort_by == SortByEnum.priority:
        priority_order = case(
            {"high": 3, "medium": 2, "low": 1},
            value=TodoDB.priority
        )
        return query.order_by(priority_order.desc() if order == OrderEnum.desc else priority_order.asc())
    return query