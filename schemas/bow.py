from pydantic import BaseModel
import datetime
import json

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
    user_id: int
    draw_weight: float

class BowCreate(BowBase):
    pass

class BowUpdate(BowBase):
    id: int

class Bow(BowBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime
    bow_type: BowType

    class Config:
        orm_mode = True

class BowCreateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BowCreate):
            return {"name": obj.name, "user_id": obj.user_id, "bow_type_id": obj.bow_type_id, "draw_weight": obj.draw_weight}
        return super().default(obj)