
from fastapi import APIRouter, Depends, HTTPException, status
from db.dals.end_dal import EndDAL
from routes.schemas.end import EndCreate, EndUpdate
from routes.dependencies import get_end_dal, get_token_user

router = APIRouter()

##
## Authorization: User is only allowed to create ends for themselves
@router.post("/user/{user_id}/round/{round_id}/end", response_model=None)
def create_end(user_id: int, round_id:int, end: EndCreate, end_dal: EndDAL = Depends(get_end_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return end_dal.create_end(round_id=round_id, end=end)

##
## Authorization: User is only allowed to edit their ends
@router.put("/user/{user_id}/round/{round_id}/end/{end_id}", response_model=None)
def update_end(user_id: int, round_id: int, end_id: int, end: EndUpdate, end_dal: EndDAL = Depends(get_end_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return end_dal.update_end(end_id=end_id, round_id=round_id, end=end)

##
## Authorization: User is only allowed to delete their ends    
@router.delete("/user/{user_id}/round/{round_id}/end/{end_id}", response_model=None)
def delete_end(user_id: int, round_id: int, end_id: int, end_dal: EndDAL = Depends(get_end_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    return end_dal.delete_end(end_id=end_id)