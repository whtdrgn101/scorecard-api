from pydantic import BaseModel
from typing import List, Optional
import datetime
from .bow import Bow
from .end import End
from .user import User

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
    round_type: Optional[RoundType]
    score_total: int
    user: Optional[User]
    bow: Optional[Bow]
    ends: Optional[List[End]]

    class Config:
        orm_mode = True