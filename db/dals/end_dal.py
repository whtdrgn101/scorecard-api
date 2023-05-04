
from sqlalchemy import update
from sqlalchemy.orm import Session
from datetime import datetime
from db.models.end import End

class EndDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def create_end(self, round_id: int, end: End):
        new_end = End(score = end.score, round_id = round_id, created_date = datetime.now(), updated_date = datetime.now())
        self.db_session.add(new_end)
        await self.db_session.flush()

    async def update_end(self, end_id: int, end: End):
        q = update(End).where(End.id == end_id)
        q = q.values(score = end.score)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def delete_end(self, end_id: int):
        deleted_end = self.db_session.query(End).filter(End.id == end_id).first()
        self.db_session.delete(deleted_end)
        await self.db_session.flush()      