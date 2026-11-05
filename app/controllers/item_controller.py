from fastapi import APIRouter, Depends
from app.database import get_db
from app.models.item import ItemCreate
from app.services import item_service

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemCreate, status_code=201)
def create_item(item: ItemCreate, db = Depends(get_db)):
    return item_service.add_item(item, db)


@router.get("/", response_model=list[ItemCreate])
def get_items(db = Depends(get_db)):
    return item_service.get_all_items(db)


@router.get("/{item_id}", response_model=ItemCreate)
def get_item(item_id: int, db = Depends(get_db)):
    return item_service.get_item_by_id(item_id, db)

@router.get("/owner/{owner_id}", response_model=list[ItemCreate])
def get_items_by_owner(owner_id: int, db = Depends(get_db)):
    return item_service.get_items_by_owner(owner_id, db)