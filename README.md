# Todo List API

This is a simple Todo List API built with FastAPI and SQLite.

## Setup

1. Clone the repository:
```
git clone https://github.com/jecaps/ToDo-List-API.git
cd ToDo-List-Api
```
2. Create a virtual environment and activate it:
```
python -m venv .venv
source .venv/bin/activate
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

## Running the Application

To run the application, use the following command:
```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the application is running, you can view the automatic interactive API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Database

This project uses SQLite as the database. The database file (`todo_list.db`) will be created in the project root directory when you first run the application or perform a database operation.

## Models

The project includes two main models:

1. List: Represents a todo list with a title and description.
2. Todo: Represents a todo item with a title, details, completion status, and associated list.

## API Endpoints

### Lists

- **POST /lists**: Create a new list

    - Request body: 
        ```
        { 
            "title": "string", 
            "description": "string" 
        }
        ```
    - Response: Created list object


- **GET /lists**: Retrieve all lists

    - Query parameters:

        - skip: Number of records to skip (default: 0)
        - limit: Maximum number of records to return (default: 10)
        - sort_by: Sort order for lists ("asc" or "desc", default: "desc")


    - Response: Array of list objects


- **GET /lists/{id}**: Retrieve a specific list

    - Path parameter: id (integer)
    - Response: List object


- **PUT /lists/{id}**: Update a list

    - Path parameter: id (integer)
    - Request body:
        ```
        { 
            "title": "string", 
            "description": "string" 
        }
        ```
    - Response: Updated list object


- **DELETE /lists/{id}**: Delete a list

    - Path parameter: id (integer)
    - Response: No content (204)

### Todos 

- **POST /todos**: Create a new todo

    - Request body:
        ```
        { 
            "title": "string", 
            "details": "string", 
            "completed": boolean, 
            "due_date": datetime
            "priority": "high" | "medium" | "low",
            "list_id": integer, 
        }
        ```
    - Response: Created todo object


- **GET /todos**: Retrieve todos with filtering and sorting
    - Query Parameters:
        - due_date: Filter by due_date
        - priority: Filter by priority (high, medium, low)
        - sort_by: Sort by field (due_date, priority, created_at)
        - order: Sort order (asd, desc)
    - Response: Array of filtered and sorted todo objects 


- **GET /todos/{todo_id}**: Retrieve a specific todo

    - Path parameter: todo_id (integer)
    - Response: Todo object


- **PUT /todos/{todo_id}**: Update a todo

    - Path parameter: todo_id (integer)
    - Request body:
        ```
        { 
            "title": "string", 
            "details": "string", 
            "completed": boolean, 
            "due_date": datetime
            "priority": "high" | "medium" | "low",
            "list_id": integer, 
        }
        ```
    - Response: Updated todo object


- **DELETE /todos/{todo_id}**: Delete a todo

    - Path parameter: todo_id (integer)
    - Response: No content (204)

## Development

This project now includes full CRUD operations for both lists and todos, with advanced features including:

- Priority levels: (HIGH, MEDIUM, LOW)
- Due dates for todos
- Flexible sorting options (by due date, priority or creation time)
- Filtering capabilities (by due date and priority)
- Error handling for invalid list references
