import json
from .user import UserCreate
from .bow import BowCreate
from .round import RoundCreate
from .end import EndCreate
import datetime

class CreationEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UserCreate):
            return {"name": obj.name, "email": obj.email, "password": obj.password}
        if isinstance(obj, BowCreate):
            return {"name": obj.name, "user_id": obj.user_id, "bow_type_id": obj.bow_type_id, "draw_weight": obj.draw_weight}
        if isinstance(obj, RoundCreate):
            return {"user_id": obj.user_id, "round_type_id": obj.round_type_id, "bow_id": obj.bow_id, "round_date": obj.round_date}
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, EndCreate):
            return {"round_id": obj.round_id, "score": obj.score}
        return super().default(obj)