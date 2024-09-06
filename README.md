# Todo List API

This is a simple Todo List API built with FastAPI and SQLite.

## Setup

1. Clone the repository:
```
git clone <repository-url>
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
uvicorn main:app --reload
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

(You can list your main API endpoints here once they're implemented)

## Development

This project is still in development. Future updates will include implementation of CRUD operations for lists and todo items, search functionality, and more.