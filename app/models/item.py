from pydantic import BaseModel


class ItemCreate(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    owner_id: int