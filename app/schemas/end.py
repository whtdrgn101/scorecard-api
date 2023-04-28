from pydantic import BaseModel
import datetime

class EndBase(BaseModel):
    round_id: int
    score: int

class EndCreate(EndBase):
    pass

class EndUpdate(EndBase):
    id: int
    
class End(EndBase):
    id: int
    created_date: datetime.datetime
    updated_date: datetime.datetime

    class Config:
        orm_mode = True