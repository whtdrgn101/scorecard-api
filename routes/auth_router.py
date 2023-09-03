
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from db.dals.user_dal import UserDAL
from routes.schemas.auth import AuthCreate, AuthToken
from routes.dependencies import get_user_dal, get_token_user, get_refresh_token

router = APIRouter()

@router.post("/auth", response_model=None)
def auth_user(auth: AuthCreate, user_dal: UserDAL = Depends(get_user_dal)):   
    
    try: 
        result = user_dal.authenticate_user(email = auth.email, password=auth.password)
        return result
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ex.args[0]
        )

@router.post("/refresh", response_model=None)
def refresh_token(user_dal: UserDAL = Depends(get_user_dal), token_user = Depends(get_refresh_token)):
    try:
        user = user_dal.get_user(token_user['user_id'])
        if user is not None:
            return user_dal.exchange_refresh_token(user.id)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex.args[0]
        )