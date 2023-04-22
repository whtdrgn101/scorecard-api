from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

import schemas
import crud
from database import SessionLocal, engine
from models.base import Base

# Setup ORM Wrapper before app is initialized
Base.metadata.create_all(bind=engine)

# Initializes the FastAPI app
app = FastAPI()

# Dependency Injection Point for getting DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DBConn = Annotated[Session, Depends(get_db)]

##
## User API's
##
@app.get("/user/", response_model=list[schemas.User])
def read_users(db: DBConn, skip: int = 0, limit: int = 100):
    customers = crud.get_users(db = db, skip=skip, limit=limit)
    return customers

@app.get("/user/{user_id}", response_model=schemas.User)
def read_customer(db: DBConn, user_id: int):
    db_cust = crud.get_user(db = db, user_id=user_id)
    if db_cust is None:
        raise HTTPException(status_code=404, detail=f"User [{user_id}] not found")
    return db_cust

@app.post("/user/", response_model=schemas.User)
def create_user(db: DBConn, user: schemas.UserCreate):
    return crud.create_user(db = db, user = user)