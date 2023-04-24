from pydantic import BaseModel
import datetime
import json

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

class EndCreateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EndCreate):
            return {"round_id": obj.round_id, "score": obj.score}
        return super().default(obj)