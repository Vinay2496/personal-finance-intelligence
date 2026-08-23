from pydantic import BaseModel


class SummaryKPIs(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float  # percentage, e.g. 36.8 means 36.8%
    average_transaction_amount: float
    transaction_count: int
class CategoryBreakdownItem(BaseModel):
    category: str
    total_amount: float
    percentage: float
    transaction_count: int
class MonthlyTrendItem(BaseModel):
    month: str  # e.g. "2026-08"
    income: float
    expenses: float
    net_savings: float
class TopMerchantItem(BaseModel):
    merchant: str
    total_amount: float
    transaction_count: int