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
## Middleware for logging
##
@app.middleware("http")
async def log_requests(request, call_next):
    # intercept the request
    print(f"Received {request.method} request to {request.url}")
    print(request.headers)

    # call the next middleware or route
    response = await call_next(request)

    # intercept the response
    print(response)

    return response

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

@app.put("/user/{user_id}", response_model=schemas.User)
def update_user(db: DBConn, user_id: int, user: schemas.UserUpdate):
    try:
        user.id = user_id
        return crud.update_user(db = db, user = user)
    except:
        raise HTTPException(status_code=404, detail=f"User with end_id={user_id} not found.")

##
## Bow Methods
##
@app.get("/user/{user_id}/bow", response_model=list[schemas.Bow])
def get_bows_by_user(db: DBConn, user_id: int, skip: int = 0, limit: int = 100):
    return crud.get_bows_by_user(db = db, user_id=user_id, skip = skip, limit=limit)

@app.post("/user/{user_id}/bow", response_model=schemas.Bow)
def create_bow(db: DBConn, user_id: int, bow: schemas.BowCreate):
    return crud.create_bow(db = db, bow = bow)

@app.put("/user/{user_id}/bow/{bow_id}", response_model=schemas.Bow)
def update_bow(db: DBConn, user_id: int, bow_id: int, bow: schemas.BowUpdate):
    bow.id = bow_id
    bow.user_id = user_id
    try:
        return crud.update_bow(db = db, bow = bow)
    except:
        raise HTTPException(status_code=404, detail=f"Bow with bow_id={bow_id} not found.")

##
## Round Methods
##
@app.get("/user/{user_id}/round", response_model=list[schemas.Round])
def get_bows_by_user(db: DBConn, user_id: int, skip: int = 0, limit: int = 100):
    return crud.get_rounds_by_user(db = db, user_id=user_id, skip = skip, limit=limit)

@app.post("/user/{user_id}/round", response_model=schemas.Round)
def create_round(db: DBConn, user_id: int, round: schemas.RoundCreate):
    return crud.create_round(db = db, round = round)

@app.put("/user/{user_id}/round/{round_id}", response_model=schemas.Round)
def update_round(db: DBConn, user_id: int, round_id: int, round: schemas.RoundUpdate):
    round.id = round_id
    round.user_id = user_id
    try:
        return crud.update_round(db = db, round = round)
    except:
        raise HTTPException(status_code=404, detail=f"Round with round_id={round_id} not found.")

##
## End Methods
##
@app.post("/user/{user_id}/round/{round_id}/end", response_model=schemas.End)
def create_end(db: DBConn, user_id: int, end: schemas.EndCreate):
    return crud.create_end(db = db, end = end)

@app.put("/user/{user_id}/round/{round_id}/end/{end_id}", response_model=schemas.End)
def update_end(db: DBConn, user_id: int, round_id: int, end_id: int, end: schemas.EndUpdate):
    end.id = end_id
    end.round_id = round_id
    try:
        return crud.update_end(db = db, end = end)
    except:
        raise HTTPException(status_code=404, detail=f"End with end_id={end_id} not found.")
    
@app.delete("/user/{user_id}/round/{round_id}/end/{end_id}", response_model=schemas.Message)
def delete_end(db: DBConn, user_id: int, round_id: int, end_id: int):
    try:
        return crud.delete_end(db = db, end_id = end_id)
    except:
        raise HTTPException(status_code=404, detail=f"End with end_id={end_id} not found.")