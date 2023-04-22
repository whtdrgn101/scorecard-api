from pydantic import BaseModel
import datetime

class BowTypeBase(BaseModel):
    name: str
    active: bool

class BowTypeCreate(BowTypeBase):
    pass

class BowType(BowTypeBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True

class BowBase(BaseModel):
    name: str
    bow_type_id: int
    draw_weight: float

class BowCreate(BowBase):
    pass

class Bow(BowBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True

