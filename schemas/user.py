from pydantic import BaseModel
import datetime
import json

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    id: int

class User(UserBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True

class UserCreateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UserCreate):
            return {"name": obj.name, "email": obj.email}
        return super().default(obj)