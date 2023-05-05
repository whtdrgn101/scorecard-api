
from sqlalchemy import update, insert
from sqlalchemy.orm import Session
from datetime import datetime
from db.models.end import End

class EndDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def create_end(self, round_id: int, end: End):
        dt = datetime.now()
        q = insert(End)
        q = q.values(round_id=end.round_id)
        q = q.values(score=end.score)
        q = q.values(updated_date=dt)
        q = q.values(created_date=dt)
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        end_id = result.inserted_primary_key[0]
        new_end = End(id=end_id, round_id=end.round_id, score=end.score, updated_date=dt, created_date=dt)
        return new_end

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