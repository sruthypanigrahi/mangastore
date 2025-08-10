from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    is_active: Optional[bool]

    class Config:
        orm_mode = True

class Role(str, Enum):
    admin = "admin"
    customer = "customer"
    delivery_boy = "delivery_boy"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.customer

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class MangaBase(BaseModel):
    title: str
    author: str
    genre: List[str]
    price: float
    stock: int
    rating: Optional[float] = 0

class MangaCreate(MangaBase):
    pass

class Manga(MangaBase):
    id: str

    class Config:
        orm_mode = True

class Review(BaseModel):
    user_id: str
    manga_id: str
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class Order(BaseModel):
    user_id: str
    manga_ids: List[str]
    total_price: float
    status: str = "pending"

class OrderCreate(BaseModel):
    user_id: str
    manga_ids: List[str]
    total_price: float
    status: Optional[str] = "pending"