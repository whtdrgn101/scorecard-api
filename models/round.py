from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .bow import Bow

class RoundType(Base):
    __tablename__ = "round_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=False)
    active = Column(Boolean, unique=False, index=True)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)

    
class Round(Base):
    __tablename__ = "round"

    id = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    bow_id: Mapped[int] = mapped_column(ForeignKey("bow.id"))
    round_type_id: Mapped[int] = mapped_column(ForeignKey("round_type.id"))
    round_date = Column(Date, unique=False, index=False)
    score_total = Column(Integer, unique=False, index=False)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)

    round_type: Mapped[RoundType] = relationship()
    bow: Mapped[Bow] = relationship()
