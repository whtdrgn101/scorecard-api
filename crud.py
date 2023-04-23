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

def update_user(db: Session, user: schemas.User):
    usr = db.query(models.User).filter(models.User.id == user.id).first()
    usr.name = user.name
    usr.email = user.email
    usr.updated_date = datetime.now()
    db.commit()
    db.refresh(usr)
    return usr
    
###
### Bow Methods
###
def get_bows_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Bow).filter(models.Bow.user_id == user_id).offset(skip).limit(limit).all()

def create_bow(db: Session, bow: schemas.BowCreate):
    new_bow = models.Bow(bow_type_id = bow.bow_type_id, user_id = bow.user_id, name = bow.name,  draw_weight = bow.draw_weight, created_date = datetime.now(), updated_date = datetime.now())
    db.add(new_bow)
    db.commit()
    db.refresh(new_bow)
    return new_bow

def update_bow(db: Session, bow: schemas.Bow):
    bow_changed = db.query(models.Bow).filter(models.Bow.id == bow.id).first()
    bow_changed.bow_type_id = bow.bow_type_id
    bow_changed.user_id = bow.user_id
    bow_changed.name = bow.name
    bow_changed.draw_weight = bow.draw_weight
    bow_changed.updated_date = datetime.now()
    db.commit()
    db.refresh(bow_changed)
    return bow_changed

###
### Round Methods
###
def get_rounds_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Round).filter(models.Round.user_id == user_id).offset(skip).limit(limit).all()

def create_round(db: Session, round: schemas.RoundCreate):
    new_round = models.Round(round_type_id = round.round_type_id, user_id = round.user_id, bow_id = round.bow_id, round_date = round.round_date, score_total = 0, created_date = datetime.now(), updated_date = datetime.now())
    db.add(new_round)
    db.commit()
    db.refresh(new_round)
    return new_round

def update_round(db: Session, round: schemas.Round):
    round_changed = db.query(models.Round).filter(models.Round.id == round.id).first()
    round_changed.bow_id = round.bow_id
    round_changed.round_date = round.round_date
    round_changed.round_type_id = round.round_type_id
    round_changed.updated_date = datetime.now()
    db.commit()
    db.refresh(round_changed)
    return round_changed