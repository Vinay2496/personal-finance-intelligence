from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    deadline = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())