from db.config import session
from db.dals.user_dal import UserDAL, ALGORITHM, JWT_SECRET_KEY
from db.dals.bow_dal import BowDAL
from db.dals.round_dal import RoundDAL
from db.dals.end_dal import EndDAL
from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth",
    scheme_name="JWT"
)

def get_user_dal():
    db = session()
    try:
        with db.begin():
            yield UserDAL(db)
    finally:
        db.close()

def get_bow_dal():
    with session() as session:
        with session.begin():
            yield BowDAL(session)

def get_round_dal():
    with session() as session:
        with session.begin():
            yield RoundDAL(session)

def get_end_dal():
    with session() as session:
        with session.begin():
            yield EndDAL(session)

def get_token_user(token: str = Depends(reuseable_oauth)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
                
        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload