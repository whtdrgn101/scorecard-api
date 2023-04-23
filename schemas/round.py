from pydantic import BaseModel
import datetime
from .bow import Bow

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

    class Config:
        orm_mode = True