
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from db.dals.user_dal import UserDAL
from routes.schemas.auth import AuthCreate, AuthToken
from routes.dependencies import get_user_dal

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
