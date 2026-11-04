from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    items = relationship("ItemDB", back_populates="owner")

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserDB", back_populates="items")