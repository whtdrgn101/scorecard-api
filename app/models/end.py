from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class End(Base):
    __tablename__ = "end"

    id = Column(Integer, primary_key=True, index=True)
    round_id: Mapped[int] = mapped_column(ForeignKey("round.id"))
    score = Column(Integer, primary_key=False, index=False)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)