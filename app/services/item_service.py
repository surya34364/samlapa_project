from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ORM_models import ItemDB, UserDB
from app.models.item import ItemCreate


def add_item(data: ItemCreate, db = Depends(get_db)):
    if db.query(ItemDB).filter(ItemDB.id == data.id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")
    if not db.query(UserDB).filter(UserDB.id == data.owner_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner does not exist")
    item = ItemDB(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_item_by_id(item_id: int, db = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

def get_items_by_owner(owner_id: int, db = Depends(get_db)):
    owner = db.query(ItemDB).filter(ItemDB.owner_id == owner_id).all()
    if not owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner does not exist")
    return owner


def get_all_items(db = Depends(get_db)):
    return db.query(ItemDB).all()