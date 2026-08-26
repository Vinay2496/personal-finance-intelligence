from sqlalchemy.orm import Session

from app.services.analytics import (
    get_summary_kpis,
    get_category_breakdown,
    get_monthly_trend,
    get_top_merchants,
)
from app.services.intelligence import (
    get_month_comparison,
    get_recurring_expenses,
    get_unusual_transactions,
)
from app.services.forecasting import get_spending_forecast


def tool_get_monthly_spending(user_id: int, db: Session) -> dict:
    """Returns income/expenses/savings for each month on record."""
    return {"monthly_trend": get_monthly_trend(user_id, db)}


def tool_get_category_spending(user_id: int, db: Session) -> dict:
    """Returns total spending broken down by category."""
    return {"category_breakdown": get_category_breakdown(user_id, db)}


def tool_compare_months(user_id: int, db: Session) -> dict:
    """Compares the most recent month's spending to the previous month."""
    return get_month_comparison(user_id, db) or {"note": "Not enough data to compare months."}


def tool_get_top_merchants(user_id: int, db: Session, limit: int = 10) -> dict:
    """Returns the merchants the user spent the most money at."""
    return {"top_merchants": get_top_merchants(user_id, db, limit=limit)}


def tool_get_recurring_expenses(user_id: int, db: Session) -> dict:
    """Returns expenses that repeat monthly (subscriptions, rent, etc.)."""
    return {"recurring_expenses": get_recurring_expenses(user_id, db)}


def tool_get_unusual_transactions(user_id: int, db: Session) -> dict:
    """Returns transactions that are statistically unusual (much larger than typical)."""
    return {"unusual_transactions": get_unusual_transactions(user_id, db)}


def tool_forecast_spending(user_id: int, db: Session) -> dict:
    """Returns a forecast of next month's expenses."""
    return get_spending_forecast(user_id, db)


def tool_get_savings_rate(user_id: int, db: Session) -> dict:
    """Returns overall income, expenses, savings amount, and savings rate percentage."""
    return get_summary_kpis(user_id, db)


# Registry: maps tool name (as given to Gemini) to the actual function
TOOL_REGISTRY = {
    "get_monthly_spending": tool_get_monthly_spending,
    "get_category_spending": tool_get_category_spending,
    "compare_months": tool_compare_months,
    "get_top_merchants": tool_get_top_merchants,
    "get_recurring_expenses": tool_get_recurring_expenses,
    "get_unusual_transactions": tool_get_unusual_transactions,
    "forecast_spending": tool_forecast_spending,
    "get_savings_rate": tool_get_savings_rate,
}