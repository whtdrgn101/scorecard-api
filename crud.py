from sqlalchemy.orm import Session
from datetime import datetime

import schemas
import models

###
### User Methods
###
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(name = user.name, email = user.email, created_date = datetime.now(), updated_date = datetime.now())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
