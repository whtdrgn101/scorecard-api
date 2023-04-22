from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True

