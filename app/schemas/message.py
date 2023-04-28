from pydantic import BaseModel
import datetime

class Message(BaseModel):
    message: str
    message_date: datetime.datetime