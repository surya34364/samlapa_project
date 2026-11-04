from pydantic import BaseModel


class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None = None
    is_active: bool = True
    