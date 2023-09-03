
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from db.dals.user_dal import UserDAL
from routes.schemas import User, UserCreate, UserUpdate
from routes.dependencies import get_user_dal, get_token_user

router = APIRouter()

##
## Authorization - All Users
@router.get("/user", response_model=List[User])
def get_all_users(skip: Optional[int] = 0, limit: Optional[int] = 100, user_dal: UserDAL = Depends(get_user_dal), token_user = Depends(get_token_user)) -> List[User]:
    try:
        return user_dal.get_all_users()
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.args[0]
        )

##
## Authorization - Only same user can request their info
@router.get("/user/{user_id}", response_model=User)
def read_customer(user_id: int, user_dal: UserDAL = Depends(get_user_dal), token_user = Depends(get_token_user)) -> User:
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    
    try:
        return user_dal.get_user(user_id)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.args[0]
        )

##
## Authorization - None
@router.post("/user", response_model=None)
def create_user(user: UserCreate, user_dal: UserDAL = Depends(get_user_dal)):
    try:
        return user_dal.create_user(user)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.args[0]
        )


##
## Authorization - Only same user can update their info
@router.put("/user/{user_id}", response_model=None)
def update_user(user_id: int, user: UserUpdate, user_dal: UserDAL = Depends(get_user_dal), token_user = Depends(get_token_user)):
    if int(token_user['user_id']) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )
    try:
        return user_dal.update_user(user_id, user)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.args[0]
        )