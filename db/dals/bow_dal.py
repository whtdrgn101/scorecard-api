
from typing import List, Optional
from sqlalchemy import update, insert, delete
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from db.models.bow import Bow, BowType

class BowDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def get_bow_types(self) -> List[BowType]:
        q = await self.db_session.execute(select(BowType).where(BowType.active == True))
        return q.scalars().all()

    async def get_bows_by_user(self, user_id: int, skip: Optional[int] = 0, limit: Optional[int] = 100) -> List[Bow]:
        q = await self.db_session.execute(
            select(Bow).filter(Bow.user_id == user_id).offset(skip).limit(limit)
                .options(joinedload(Bow.bow_type))
        )
        return q.scalars().all()
    
    async def get_bow_by_user(self, user_id: int, bow_id: int) -> Bow:
        q = await self.db_session.execute(
            select(Bow).filter(Bow.user_id == user_id, Bow.id == bow_id)
                .options(joinedload(Bow.bow_type))
        )
        return q.scalar()

    async def create_bow(self, user_id: int, bow: Bow) -> Bow:
        dt = datetime.now()
        q = insert(Bow)
        q = q.values(name=bow.name)
        q = q.values(user_id=bow.user_id)
        q = q.values(bow_type_id=bow.bow_type_id)
        q = q.values(draw_weight=bow.draw_weight)
        q = q.values(updated_date=dt)
        q = q.values(created_date=dt)
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        bow_id = result.inserted_primary_key[0]
        new_bow = Bow(id=bow_id, user_id=bow.user_id, bow_type_id=bow.bow_type_id, draw_weight=bow.draw_weight, updated_date=dt, created_date=dt)
        return new_bow

    async def update_bow(self, bow_id: int, user_id: int, bow: Bow):
        q = update(Bow).where(Bow.id == bow_id, Bow.user_id == user_id)
        q = q.values(bow_type_id=bow.bow_type_id)
        q = q.values(user_id=bow.user_id)
        q = q.values(name=bow.name)
        q = q.values(draw_weight=bow.draw_weight)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        return result

    async def delete_bow(self, bow_id:int, user_id: int):
        q = delete(Bow).where(Bow.id == bow_id, Bow.user_id == user_id)
        result = await self.db_session.execute(q)
        return result
