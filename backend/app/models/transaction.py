from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    transaction_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    merchant = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # "debit" or "credit"
    category = Column(String, nullable=True)
    subcategory = Column(String, nullable=True)
    source_file = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())