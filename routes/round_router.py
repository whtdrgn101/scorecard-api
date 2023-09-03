from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from db.dals.round_dal import RoundDAL
from routes.schemas.round import RoundCreate, RoundUpdate, Round, RoundType
from routes.schemas.message import Message
from routes.dependencies import get_round_dal, get_token_user
from datetime import datetime

router = APIRouter()

##
## Authorization: None
@router.get("/round-type", response_model=List[RoundType])
def read_round_types(round_dal: RoundDAL = Depends(get_round_dal)) -> List[RoundType]:
    return round_dal.get_round_types()

##
## Authorization: User is only allowed to get their own rounds
@router.get("/user/{user_id}/round", response_model=List[Round])
def get_rounds_by_user_id(user_id: int, skip: int = 0, limit: int = 100, round_dal: RoundDAL = Depends(get_round_dal), token_user = Depends(get_token_user)) -> List[Round]:
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return round_dal.get_rounds_by_user(user_id=user_id, skip = skip, limit = limit)

##
## Authorization: User is only allowed to get their own rounds
@router.get("/user/{user_id}/round/{round_id}", response_model=Round)
def get_round_by_user_by_round(user_id: int, round_id: int, round_dal: RoundDAL = Depends(get_round_dal), token_user = Depends(get_token_user)) -> Round:
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return round_dal.get_round_by_user_round(user_id=user_id, round_id=round_id)

##
## Authorization: User can only create rounds for themselves      
@router.post("/user/{user_id}/round", response_model=Round)
def create_round(user_id: int, round: RoundCreate, round_dal: RoundDAL = Depends(get_round_dal), token_user = Depends(get_token_user)):
   if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
   return round_dal.create_round(user_id, round)

##
## Authorization: User can only edit their rounds 
@router.put("/user/{user_id}/round/{round_id}", response_model=Message)
def update_round(user_id: int, round_id: int, round: RoundUpdate, round_dal: RoundDAL = Depends(get_round_dal), token_user = Depends(get_token_user)): 
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    
    result = round_dal.update_round(round_id, user_id, round)
    if result.rowcount > 0:
        return Message(message="Round changes saved", message_date=datetime.now())
    else:
        raise HTTPException(404, detail=f"Unable to update round: {round_id}")

##
## Authorization: User can only delete their rounds
@router.delete("/user/{user_id}/round/{round_id}", response_model=Message)
def delete_round(user_id: int, round_id: int, round_dal: RoundDAL = Depends(get_round_dal), token_user = Depends(get_token_user)): 
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    result = round_dal.delete_round(round_id = round_id, user_id = user_id)
    if result.rowcount > 0:
        return Message(message="Round deleted", message_date=datetime.now())
    else:
        raise HTTPException(404, detail=f"Unable to delete round: {round_id}")