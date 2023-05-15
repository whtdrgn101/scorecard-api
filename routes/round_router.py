from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from db.config import async_session
from db.dals.round_dal import RoundDAL
from routes.schemas.round import RoundCreate, RoundUpdate, Round, RoundType
from routes.schemas.message import Message
from dependencies import get_round_dal
from datetime import datetime

router = APIRouter()

@router.get("/round-type", response_model=List[RoundType])
async def read_round_types(round_dal: RoundDAL = Depends(get_round_dal)) -> List[RoundType]:
    async with async_session() as session:
        async with session.begin():
            return await round_dal.get_round_types()

@router.get("/user/{user_id}/round", response_model=List[Round])
async def get_rounds_by_user_id(user_id: int, skip: int = 0, limit: int = 100, round_dal: RoundDAL = Depends(get_round_dal)) -> List[Round]:
    async with async_session() as session:
        async with session.begin():
            return await round_dal.get_rounds_by_user(user_id=user_id)

@router.get("/user/{user_id}/round/{round_id}", response_model=Round)
async def get_round_by_user_by_round(user_id: int, round_id: int, round_dal: RoundDAL = Depends(get_round_dal)) -> Round:
    async with async_session() as session:
        async with session.begin():
            return await round_dal.get_round_by_user_round(user_id=user_id, round_id=round_id)
        
@router.post("/user/{user_id}/round", response_model=Round)
async def create_round(user_id: int, round: RoundCreate, round_dal: RoundDAL = Depends(get_round_dal)):
    async with async_session() as session:
        async with session.begin():
            return await round_dal.create_round(user_id, round)
    
@router.put("/user/{user_id}/round/{round_id}", response_model=Message)
async def update_round(user_id: int, round_id: int, round: RoundUpdate, round_dal: RoundDAL = Depends(get_round_dal)):
    async with async_session() as session:
        async with session.begin():
            result = await round_dal.update_round(round_id, user_id, round)
            if result.rowcount > 0:
                return Message(message="Round changes saved", message_date=datetime.now())
            else:
                raise HTTPException(404, detail=f"Unable to update round: {round_id}")
        
@router.delete("/user/{user_id}/round/{round_id}", response_model=Message)
async def delete_round(user_id: int, round_id: int, round_dal: RoundDAL = Depends(get_round_dal)):
    async with async_session() as session:
        async with session.begin():
            result = await round_dal.delete_round(round_id = round_id, user_id = user_id)
            if result.rowcount > 0:
                return Message(message="Round deleted", message_date=datetime.now())
            else:
                raise HTTPException(404, detail=f"Unable to delete round: {round_id}")