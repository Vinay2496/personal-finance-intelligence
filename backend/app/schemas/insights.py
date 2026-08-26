from pydantic import BaseModel
from typing import Optional


class MonthComparison(BaseModel):
    current_month: str
    previous_month: Optional[str] = None
    current_expenses: float
    previous_expenses: Optional[float] = None
    change_amount: Optional[float] = None
    change_percent: Optional[float] = None


class CategoryChange(BaseModel):
    category: str
    current_amount: float
    previous_amount: float
    change_amount: float


class RecurringExpense(BaseModel):
    merchant: str
    average_amount: float
    occurrence_count: int
    frequency: str  # "monthly" (only type we detect for now)


class UnusualTransaction(BaseModel):
    id: int
    description: str
    merchant: Optional[str]
    amount: float
    transaction_date: str
    reason: str


class Insight(BaseModel):
    type: str  # "spending_increase", "spending_decrease", "recurring", "unusual", "saving_opportunity"
    message: str


class InsightsResponse(BaseModel):
    insights: list[Insight]
    month_comparison: Optional[MonthComparison] = None
    category_changes: list[CategoryChange] = []
    recurring_expenses: list[RecurringExpense] = []
    unusual_transactions: list[UnusualTransaction] = []