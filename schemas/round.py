from pydantic import BaseModel
from typing import List, Optional
import datetime
from .bow import Bow
from .end import End
import json

class RoundTypeBase(BaseModel):
    name: str
    active: bool

class RoundTypeCreate(RoundTypeBase):
    pass

class RoundType(RoundTypeBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True

class RoundBase(BaseModel):
    round_type_id: int
    user_id: int
    bow_id: int
    round_date: datetime.datetime
   
class RoundCreate(RoundBase):
    pass

class RoundUpdate(RoundBase):
    id: int
        
class Round(RoundBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime
    round_type: RoundType
    score_total: int
    bow: Bow
    ends: Optional[List[End]]

    class Config:
        orm_mode = True

class RoundCreateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, RoundCreate):
            return {"user_id": obj.user_id, "round_type_id": obj.round_type_id, "bow_id": obj.bow_id, "round_date": obj.round_date}
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)