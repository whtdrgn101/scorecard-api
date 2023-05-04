
from typing import List, Optional
from fastapi import APIRouter, Depends
from db.config import async_session
from db.dals.bow_dal import BowDAL
from routes.schemas import Bow, BowCreate, BowUpdate, BowType
from dependencies import get_bow_dal

router = APIRouter()

@router.get("/bow-type/", response_model=List[BowType])
async def read_bow_types(bow_dal: BowDAL = Depends(get_bow_dal)) ->List[BowType]:
    async with async_session() as session:
        async with session.begin():
            return await bow_dal.get_bow_types()

@router.get("/user/{user_id}/bow", response_model=List[Bow])
async def get_bows_by_user(user_id: int, skip: int = 0, limit: int = 100, bow_dal: BowDAL = Depends(get_bow_dal)) -> List[Bow]:
    async with async_session() as session:
        async with session.begin():
            return await bow_dal.get_bows_by_user(user_id=user_id, skip=skip, limit=limit)

@router.post("/user/{user_id}/bow", response_model=None)
async def create_bow(user_id: int, bow: BowCreate, bow_dal: BowDAL = Depends(get_bow_dal)):
    async with async_session() as session:
        async with session.begin():
            return await bow_dal.create_bow(user_id, bow)

@router.put("/user/{user_id}/bow/{bow_id}", response_model=None)
async def update_bow(user_id: int, bow_id: int, bow: BowUpdate, bow_dal: BowDAL = Depends(get_bow_dal)):
    async with async_session() as session:
        async with session.begin():
            return await bow_dal.update_bow(bow_id, user_id, bow)