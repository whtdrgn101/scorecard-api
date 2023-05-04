from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..config import Base

class BowType(Base):
    __tablename__ = "bow_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False)
    active = Column(Boolean, unique=False, index=True)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)

    

class Bow(Base):
    __tablename__ = "bow"

    id = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    bow_type_id: Mapped[int] = mapped_column(ForeignKey("bow_type.id"))
    name = Column(String, unique=False, index=False)
    draw_weight = Column(Float, unique=False, index=False)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)

    bow_type: Mapped[BowType] = relationship()
