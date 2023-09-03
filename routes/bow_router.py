from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from db.dals.bow_dal import BowDAL
from routes.schemas import Bow, BowCreate, BowUpdate, BowType
from routes.schemas.message import Message
from routes.dependencies import get_bow_dal, get_token_user
from datetime import datetime
router = APIRouter()

##
## Authorization: None
@router.get("/bow-type", response_model=List[BowType])
def read_bow_types(bow_dal: BowDAL = Depends(get_bow_dal)) ->List[BowType]:
    return bow_dal.get_bow_types()

##
## Authorization: User can only get bows belonging to them
@router.get("/user/{user_id}/bow", response_model=List[Bow])
def get_bows_by_user(user_id: int, skip: int = 0, limit: int = 100, bow_dal: BowDAL = Depends(get_bow_dal), token_user = Depends(get_token_user)) -> List[Bow]:
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return bow_dal.get_bows_by_user(user_id=user_id, skip=skip, limit=limit)

##
## Authorization: User can only get bows belonging to them
@router.get("/user/{user_id}/bow/{bow_id}", response_model=Bow)
def get_bow_by_user(user_id: int, bow_id: int, bow_dal: BowDAL = Depends(get_bow_dal), token_user = Depends(get_token_user)) -> Bow:
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return bow_dal.get_bow_by_user(user_id, bow_id)

##
## Authorization: User can only get bows belonging to them        
@router.post("/user/{user_id}/bow", response_model=None)
def create_bow(user_id: int, bow: BowCreate, bow_dal: BowDAL = Depends(get_bow_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return bow_dal.create_bow(user_id, bow)

##
## Authorization: User can only get bows belonging to them
@router.put("/user/{user_id}/bow/{bow_id}", response_model=None)
def update_bow(user_id: int, bow_id: int, bow: BowUpdate, bow_dal: BowDAL = Depends(get_bow_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    result = bow_dal.update_bow(bow_id, user_id, bow)
    if result.rowcount > 0:
        return Message(message="Round deleted", message_date=datetime.now())
    else:
        raise HTTPException(404, detail=f"Unable to update bow: {bow_id}")

##
## Authorization: User can only get bows belonging to them
@router.delete("/user/{user_id}/bow/{bow_id}", response_model=None)
def delete_bow(user_id: int, bow_id: int, bow_dal: BowDAL = Depends(get_bow_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    result =  bow_dal.delete_bow(bow_id=bow_id, user_id=user_id)
    if result.rowcount > 0:
        return Message(message="Round deleted", message_date=datetime.now())
    else:
        raise HTTPException(404, detail=f"Unable to delete bow: {bow_id}")