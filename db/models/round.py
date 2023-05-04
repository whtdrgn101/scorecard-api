from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..config import Base
from .bow import Bow
from .end import End
from .user import User

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
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    bow_id = mapped_column(Integer, ForeignKey("bow.id"))
    round_type_id = mapped_column(Integer, ForeignKey("round_type.id"))
    round_date = Column(Date, unique=False, index=False)
    score_total = Column(Integer, unique=False, index=False)
    created_date = Column(Date, unique=False, index=False)
    updated_date = Column(Date, unique=False, index=False)

    user: Mapped[User] = relationship(User, foreign_keys=[user_id])
    round_type: Mapped[RoundType] = relationship(RoundType, foreign_keys=[round_type_id])
    bow: Mapped[Bow] = relationship(Bow, foreign_keys=[bow_id])
    ends: Mapped[list[End]] = relationship()
