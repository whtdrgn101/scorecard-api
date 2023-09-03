from pydantic import BaseModel
from typing import Optional
import datetime

class AuthBase(BaseModel):
    email: str
    password: Optional[str]

class AuthCreate(AuthBase):
    pass

class AuthToken():
    access_token: str
    refresh_token: str