
from sqlalchemy import update, insert, delete
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

    async def update_end(self, end_id: int, round_id: int, end: End):
        q = update(End).where(End.id == end_id, End.round_id == round_id)
        q = q.values(score = end.score)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        return result

    async def delete_end(self, end_id: int):
        q = delete(End).where(End.id == end_id)
        result = await self.db_session.execute(q)
        return result     