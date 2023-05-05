
from typing import List, Optional

from sqlalchemy import update, insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session, joinedload, subqueryload
from datetime import datetime
from db.models.round import Round, RoundType
from db.models.bow import Bow, BowType
from db.models.end import End

class RoundDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def get_round_types(self) ->List[RoundType]:
        q = await self.db_session.execute(select(RoundType))
        return q.scalars().all()

    async def get_rounds_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Round]:
        q = await self.db_session.execute(
            select(Round).filter(Round.user_id == user_id).offset(skip).limit(limit)
                .options(joinedload(Round.user))
                .options(joinedload(Round.round_type))
                .options(joinedload(Round.bow).joinedload(Bow.bow_type))
                .options(subqueryload(Round.ends))      
        )
        return q.scalars().all()

    async def get_round_by_user_round(self, user_id: int, round_id: int):
        q = await self.db_session.execute(
            select(Round).filter(Round.user_id == user_id, Round.id == round_id)
                .options(joinedload(Round.user))
                .options(joinedload(Round.round_type))
                .options(joinedload(Round.bow).joinedload(Bow.bow_type))
                .options(subqueryload(Round.ends))
        )
        return q.scalar()

    async def create_round(self, user_id: int, round: Round):
        new_round = Round(round_type_id = round.round_type_id, user_id = user_id, bow_id = round.bow_id, round_date = round.round_date, score_total = 0, created_date = datetime.now(), updated_date = datetime.now())
        dt = datetime.now()
        q = insert(Round)
        q = q.values(user_id=round.user_id)
        q = q.values(round_type_id=round.round_type_id)
        q = q.values(round_date=round.round_date)
        q = q.values(updated_date=dt)
        q = q.values(created_date=dt)
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        round_id = result.inserted_primary_key[0]
        new_round = Round(id=round_id, user_id=round.user_id, round_type_id=round.round_type_id, updated_date=dt, created_date=dt, score_total=0)
        return new_round

    async def update_round(self, round_id: int, user_id: int, round: Round):
        q = update(Round).where(Round.id == round_id, Round.user_id == user_id)
        q = q.values(round_type_id = round.round_type_id)
        q = q.values(round_date=round.round_date)
        q = q.values(bow_id=round.bow_id)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
