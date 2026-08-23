from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class TransactionOut(BaseModel):
    id: int
    transaction_date: date
    description: str
    merchant: Optional[str] = None
    amount: float
    transaction_type: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    source_file: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UploadSummary(BaseModel):
    total_rows: int
    inserted: int
    duplicates_skipped: int
    invalid_rows: int
    errors: list[str] = []
class TransactionCategoryUpdate(BaseModel):
    category: str
    subcategory: Optional[str] = None