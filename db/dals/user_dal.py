
from typing import List, Optional
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from datetime import datetime
from db.models.user import User

class UserDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        q = await self.db_session.execute(select(User).offset(skip).limit(limit))
        return q.scalars().all()

    async def get_user(self, user_id: int) -> User:
        q = await self.db_session.execute(select(User).filter(User.id == user_id))
        return q.scalar()

    async def create_user(self, user: User) -> User:
        new_user = User(name = user.name, email = user.email, created_date = datetime.now(), updated_date = datetime.now())
        self.db_session.add(new_user)
        await self.db_session.flush()

    async def update_user(self, user_id: int, user: User):
        q = update(User).where(User.id == user_id)
        q = q.values(name=user.name)
        q = q.values(email=user.email)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
