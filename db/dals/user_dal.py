
from typing import List, Optional
from sqlalchemy import update, insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from datetime import datetime
from db.models.user import User
import hashlib

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
        dt = datetime.now()
        q = insert(User)
        q = q.values(name=user.name)
        q = q.values(email=user.email)
        q = q.values(updated_date=dt)
        q = q.values(created_date=dt)
        q = q.values(password=self.generate_md5_hash(user.password))
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        user_id = result.inserted_primary_key[0]
        user = User(id=user_id, name=user.name, email=user.email, updated_date=dt, created_date = dt)
        return user

    async def update_user(self, user_id: int, user: User):
        q = update(User).where(User.id == user_id)
        q = q.values(name=user.name)
        q = q.values(email=user.email)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def authenticate_user(self, email:str, password:str) -> User:
        q = await self.db_session.execute(select(User).filter(User.email == email, User.password == self.generate_md5_hash(password)))
        ret = q.scalar()
        q = update(User).filter(User.id == ret.id)
        q = q.values(last_login_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        result = await self.db_session.execute(q)
        return ret

    def generate_md5_hash(self, string:str):
        md5_hash = hashlib.md5()
        md5_hash.update(string.encode('utf-8'))
        return md5_hash.hexdigest()