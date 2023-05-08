from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Mapped, relationship
from db.models.bow import Bow
from db.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, index=False)
    name = Column(String, unique=False, index=False)
    password = Column(String, unique=False, index=False)
    last_login_date = Column(Date, unique=False, index=False)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)

    bows: Mapped[list[Bow]] = relationship(Bow, cascade="all, delete")
