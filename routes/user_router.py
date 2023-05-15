
from typing import List, Optional
from fastapi import APIRouter, Depends
from db.config import async_session
from db.dals.user_dal import UserDAL
from routes.schemas import User, UserCreate, UserUpdate
from dependencies import get_user_dal

router = APIRouter()

@router.get("/user", response_model=List[User])
async def get_all_users(skip: Optional[int] = 0, limit: Optional[int] = 100, user_dal: UserDAL = Depends(get_user_dal)) -> List[User]:
    async with async_session() as session:
        async with session.begin():
            return await user_dal.get_all_users()

@router.get("/user/{user_id}", response_model=User)
async def read_customer(user_id: int, user_dal: UserDAL = Depends(get_user_dal)) -> User:
    async with async_session() as session:
        async with session.begin():
            return await user_dal.get_user(user_id)

@router.post("/user", response_model=None)
async def create_user(user: UserCreate, user_dal: UserDAL = Depends(get_user_dal)):
    async with async_session() as session:
        async with session.begin():
            return await user_dal.create_user(user)

@router.put("/user/{user_id}", response_model=None)
async def update_user(user_id: int, user: UserUpdate, user_dal: UserDAL = Depends(get_user_dal)):
    async with async_session() as session:
        async with session.begin():
            return await user_dal.update_user(user_id, user)