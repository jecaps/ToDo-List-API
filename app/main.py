from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import list, todo

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")

app = FastAPI()

app.include_router(list.router)
app.include_router(todo.router)

@app.get("/")
def read_root():
    return {"Hello": "World"} 