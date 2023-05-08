from pydantic import BaseModel
import datetime
from .bow import Bow

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    id: int

class User(UserBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True