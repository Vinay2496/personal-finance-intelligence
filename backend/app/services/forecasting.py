from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.transaction import Transaction


def _get_monthly_expenses(user_id: int, db: Session) -> list[tuple[str, float]]:
    rows = db.execute(
        select(
            func.to_char(Transaction.transaction_date, "YYYY-MM").label("month"),
            func.sum(Transaction.amount),
        )
        .where(Transaction.user_id == user_id, Transaction.transaction_type == "debit")
        .group_by("month")
        .order_by("month")
    ).all()
    return [(row[0], float(row[1])) for row in rows]


def _next_month_str(month_str: str) -> str:
    year, month = map(int, month_str.split("-"))
    if month == 12:
        return f"{year + 1}-01"
    return f"{year}-{month + 1:02d}"


def _moving_average_forecast(values: list[float], window: int = 3) -> float:
    recent = values[-window:] if len(values) >= window else values
    return sum(recent) / len(recent)


def _exponential_smoothing_forecast(values: list[float], alpha: float = 0.5) -> float:
    smoothed = values[0]
    for v in values[1:]:
        smoothed = alpha * v + (1 - alpha) * smoothed
    return smoothed


def _evaluate_method(values: list[float], forecast_fn, **kwargs) -> float | None:
    """
    Simple backtest: for each point after the first 2, predict it using
    only prior data, then compute MAE across those predictions.
    """
    if len(values) < 3:
        return None

    errors = []
    for i in range(2, len(values)):
        history = values[:i]
        predicted = forecast_fn(history, **kwargs)
        actual = values[i]
        errors.append(abs(predicted - actual))

    return sum(errors) / len(errors) if errors else None


def get_spending_forecast(user_id: int, db: Session) -> dict:
    monthly = _get_monthly_expenses(user_id, db)
    historical_months_used = len(monthly)

    if historical_months_used < 2:
        return {
            "forecast_month": None,
            "predicted_expenses": None,
            "method_used": None,
            "reliable": False,
            "reliability_note": (
                "Not enough historical data to generate a forecast. "
                "At least 2 months of transaction history are needed."
            ),
            "mae": None,
            "historical_months_used": historical_months_used,
        }

    values = [v for _, v in monthly]
    last_month = monthly[-1][0]
    forecast_month = _next_month_str(last_month)

    # Evaluate both methods, pick the one with lower error (if evaluable)
    ma_error = _evaluate_method(values, _moving_average_forecast, window=3)
    es_error = _evaluate_method(values, _exponential_smoothing_forecast, alpha=0.5)

    if ma_error is not None and es_error is not None:
        if ma_error <= es_error:
            method_used = "moving_average"
            predicted = _moving_average_forecast(values, window=3)
            mae = ma_error
        else:
            method_used = "exponential_smoothing"
            predicted = _exponential_smoothing_forecast(values, alpha=0.5)
            mae = es_error
    else:
        # Not enough data to backtest reliably — use moving average as the safe default
        method_used = "moving_average"
        predicted = _moving_average_forecast(values, window=3)
        mae = None

    reliable = historical_months_used >= 4 and mae is not None
    if reliable:
        reliability_note = (
            f"Based on {historical_months_used} months of data. "
            f"Historical average prediction error (MAE): ₹{mae:.0f}."
        )
    else:
        reliability_note = (
            f"Only {historical_months_used} month(s) of data available. "
            "This forecast is a rough estimate and may not be accurate. "
            "Accuracy will improve as more transaction history is added."
        )

    return {
        "forecast_month": forecast_month,
        "predicted_expenses": round(predicted, 2),
        "method_used": method_used,
        "reliable": reliable,
        "reliability_note": reliability_note,
        "mae": round(mae, 2) if mae is not None else None,
        "historical_months_used": historical_months_used,
    }