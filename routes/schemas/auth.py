from pydantic import BaseModel
from typing import Optional
import datetime

class AuthBase(BaseModel):
    email: str
    password: Optional[str]

class AuthCreate(AuthBase):
    pass

class Auth(AuthBase):
    user_id: int
    last_login_date: datetime.datetime