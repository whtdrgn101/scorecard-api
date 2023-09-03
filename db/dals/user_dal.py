
import os
from typing import List, Optional
from sqlalchemy import update, insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from datetime import datetime
from db.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']    # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAL():
    def __init__(self, db_session:Session):
        self.db_session = db_session

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        q = self.db_session.execute(select(User).offset(skip).limit(limit))
        return q.scalars().all()

    def get_user(self, user_id: int) -> User:
        q = self.db_session.execute(select(User).filter(User.id == user_id))
        return q.scalar()

    def create_user(self, user: User) -> User:
        #Look for existing user
        existing = self.db_session.query(User).filter(User.email == user.email).first()
        if existing is not None:
            raise Exception(f"User already created for email address [{user.email}]")
        
        dt = datetime.now()
        q = insert(User)
        q = q.values(name=user.name)
        q = q.values(email=user.email)
        q = q.values(updated_date=dt)
        q = q.values(created_date=dt)
        q = q.values(password=self.get_hashed_password(user.password))
        q.execution_options(synchronize_session="fetch")
        result = self.db_session.execute(q)
        user_id = result.inserted_primary_key[0]
        user = User(id=user_id, name=user.name, email=user.email, updated_date=dt, created_date = dt)
        return user

    def update_user(self, user_id: int, user: User):
        q = update(User).where(User.id == user_id)
        q = q.values(name=user.name)
        q = q.values(email=user.email)
        q = q.values(updated_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        return self.db_session.execute(q)

    def authenticate_user(self, email:str, password:str) -> User:
        existing = self.db_session.query(User).filter(User.email == email).first()
        
        if existing is None:
            raise Exception("Invalid username or password")
        
        if not self.verify_password(password, existing.password):
            raise Exception("Invalid username or password")
        
        q = update(User).filter(User.id == existing.id)
        q = q.values(last_login_date=datetime.now())
        q.execution_options(synchronize_session="fetch")
        self.db_session.execute(q)

        return {
            "access_token": self.create_access_token(existing),
            "refresh_token": self.create_refresh_token(existing)
        }

    def get_hashed_password(self, password: str) -> str:
        return password_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    def create_access_token(self, user: User, expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "user_id": str(user.id), "email": str(user.email )}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, user: User, expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "user_id": str(user.id), "email": str(user.email )}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt
    