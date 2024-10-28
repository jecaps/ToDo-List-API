from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from app.schemas import ListCreate, TodoCreate, sanitize_str
from app.todo_manager import PriorityEnum


def test_sanitize_string():
    assert sanitize_str("<script>alert('xss')</script>") == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"
    assert sanitize_str("  multiple     spaces  ") == "multiple spaces"
    assert sanitize_str(None) is None

def test_todo_validation():
    # Test valid todo
    valid_todo = {
        "title": "Test Todo",
        "details": "Test Details",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "priority": "high",
        "list_id": 1
    }
    todo = TodoCreate(**valid_todo)
    assert todo.title == "Test Todo"
    assert todo.priority == PriorityEnum.HIGH

    # Test invalid due date
    with pytest.raises(ValidationError) as exc_info:
        TodoCreate(**{
            **valid_todo,
            "due_date": (datetime.now() - timedelta(days=1)).isoformat()
        })
    assert "Due date cannot be in the past" in str(exc_info.value)

    # Test invalid priority
    with pytest.raises(ValidationError) as exc_info:
        TodoCreate(**{
            **valid_todo,
            "priority": "INVALID"
        })
    assert "Input should be 'high', 'medium' or 'low'" in str(exc_info.value)

    # Test title length validation
    with pytest.raises(ValidationError) as exc_info:
        TodoCreate(**{
            **valid_todo,
            "title": "a" * 101
        })
    assert "String should have at most 100 characters" in str(exc_info.value)

def test_list_validation():
    # Test valid list
    valid_list = {
        "title": "Test List",
        "description": "Test Description"
    }
    list_item = ListCreate(**valid_list)
    assert list_item.title == "Test List"

    # Test HTML sanitization
    list_with_html = ListCreate(
        title="<b>Test</b>",
        description="<script>alert('xss')</script>"
    )
    assert list_with_html.title == "&lt;b&gt;Test&lt;/b&gt;"
    assert list_with_html.description == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;"