from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.database import get_db
from app.models import ListDB
from app.schemas import List, ListCreate

router = APIRouter(prefix="/lists", tags=["Lists"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_list(list: ListCreate, db: Session = Depends(get_db)) -> List:
    new_list = ListDB(**list.model_dump())
    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return new_list


@router.get("/")
def read_lists(skip: int = 0, limit: int = 10, sort_by: str = "desc", db: Session = Depends(get_db))   -> list[List]:
    lists_db = db.query(ListDB)

    if sort_by == "asc":
        lists_db = lists_db.order_by(ListDB.updated_at.asc())
    elif sort_by == "desc":
        lists_db = lists_db.order_by(ListDB.updated_at.desc())

    lists = lists_db.offset(skip).limit(limit).all()

    return lists


@router.get("/{id}")
def read_list(id: int, db: Session = Depends(get_db)) -> List:
    try:
        list_db = db.query(ListDB).filter(ListDB.id == id).one()
        return list_db
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {id} not found.")


@router.put("/{id}")
def update_list(id: int, list: ListCreate, db: Session = Depends(get_db))  -> List:
    list_db = db.query(ListDB).filter(ListDB.id == id)
    list_to_update = list_db.first()
        
    if list_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {id} not found.")
        
    list_db.update(list.model_dump())
    db.commit()
    db.refresh(list_to_update)

    return list_to_update


@router.delete("/{id}")
def delete_list(id: int, db: Session = Depends(get_db)) -> Response:
    list_db = db.query(ListDB).filter(ListDB.id == id).one_or_none()

    if list_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"List with id no. {id} not found.")
    
    db.delete(list_db)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)