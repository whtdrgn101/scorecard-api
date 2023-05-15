
from fastapi import APIRouter, Depends
from db.config import async_session
from db.dals.end_dal import EndDAL
from routes.schemas.end import EndCreate, EndUpdate
from routes.dependencies import get_end_dal

router = APIRouter()

@router.post("/user/{user_id}/round/{round_id}/end", response_model=None)
async def create_end(user_id: int, round_id:int, end: EndCreate, end_dal: EndDAL = Depends(get_end_dal)):
    async with async_session() as session:
        async with session.begin():
            return await end_dal.create_end(round_id=round_id, end=end)

@router.put("/user/{user_id}/round/{round_id}/end/{end_id}", response_model=None)
async def update_end(user_id: int, round_id: int, end_id: int, end: EndUpdate, end_dal: EndDAL = Depends(get_end_dal)):
    async with async_session() as session:
        async with session.begin():
            return await end_dal.update_end(end_id=end_id, round_id=round_id, end=end)
    
@router.delete("/user/{user_id}/round/{round_id}/end/{end_id}", response_model=None)
async def delete_end(user_id: int, round_id: int, end_id: int, end_dal: EndDAL = Depends(get_end_dal)):
    async with async_session() as session:
        async with session.begin():
            return await end_dal.delete_end(end_id=end_id)