
from typing import List, Optional
from fastapi import APIRouter, Depends
from db.config import async_session
from db.dals.user_dal import UserDAL
from routes.schemas.auth import AuthCreate, Auth
from dependencies import get_user_dal

router = APIRouter()

@router.post("/auth", response_model=Auth)
async def auth_user(auth: AuthCreate, user_dal: UserDAL = Depends(get_user_dal)):
    async with async_session() as session:
        async with session.begin():
            result = await user_dal.authenticate_user(email = auth.email, password=auth.password)
            auth = Auth(email=result.email, name=result.name, last_login_date=result.last_login_date, user_id=result.id)
            return auth
