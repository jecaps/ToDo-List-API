from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import List
from app.schemas import List as ListSchema
from app.schemas import ListCreate, ListWithoutTodos

router = APIRouter(prefix="/lists", tags=["Lists"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_list(list: ListCreate, db: Session = Depends(get_db)) -> ListWithoutTodos:
    new_list = List(**list.model_dump())

    if new_list.title == "":    
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required.")

    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return new_list


@router.get("/")
def read_lists(skip: int = 0, limit: int = 10, sort_by: str = "desc", db: Session = Depends(get_db)) -> list[ListSchema]:
    query = db.query(List)

    if sort_by == "asc":
        query = query.order_by(List.updated_at.asc())
    elif sort_by == "desc":
        query = query.order_by(List.updated_at.desc())

    lists = query.offset(skip).limit(limit).all()

    return lists


@router.get("/{id}")
def read_list(id: int, db: Session = Depends(get_db)) -> ListSchema:
    list = db.query(List).filter(List.id == id).first()

    if list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {id} not found.")
    
    return list


@router.put("/{id}")
def update_list(id: int, list: ListCreate, db: Session = Depends(get_db))  -> ListSchema | None:
    list_query = db.query(List).filter(List.id == id)
    list_to_update = list_query.first()

    if list_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {id} not found.")
    
    list_query.update(list.model_dump())
    db.commit()
    db.refresh(list_to_update)

    return list_to_update


@router.delete("/{id}")
def delete_list(id: int, db: Session = Depends(get_db)) -> Response:
    list_query = db.query(List).filter(List.id == id)
    list = list_query.first()

    if list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {id} not found.")
    
    list_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)