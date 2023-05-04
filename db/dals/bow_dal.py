
from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from datetime import datetime
from db.models.bow import Bow, BowType

class BowDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def get_bow_types(self) -> List[BowType]:
        q = await self.db_session.execute(select(BowType))
        return q.scalars().all()

    async def get_bows_by_user(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[Bow]:
        q = await self.db_session.execute(select(Bow).filter(Bow.user_id == user_id).offset(skip).limit(limit))
        return q.scalars().all()

    async def create_bow(self, user_id: int, bow: Bow):
        new_bow = Bow(bow_type_id = bow.bow_type_id, user_id = user_id, name = bow.name,  draw_weight = bow.draw_weight, created_date = datetime.now(), updated_date = datetime.now())
        self.db_session.add(new_bow)
        self.db_session.flush()
        self.db_session.refresh(new_bow)
        return new_bow

    async def update_bow(self, bow_id: int, user_id: int, bow: Bow):
        q = update(Bow).where(Bow.id == bow_id, Bow.user_id == user_id)
        q = q.values(bow_type_id=bow.bow_type_id)
        q = q.values(user_id=bow.user_id)
        q = q.values(name=bow.name)
        q = q.values(draw_weight=bow.draw_weight)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
