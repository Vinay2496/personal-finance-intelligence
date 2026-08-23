from sqlalchemy.orm import Session
from sqlalchemy import select, func, extract

from app.models.transaction import Transaction


def get_summary_kpis(user_id: int, db: Session) -> dict:
    income_result = db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "credit",
        )
    ).scalar()

    expenses_result = db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "debit",
        )
    ).scalar()

    total_income = float(income_result)
    total_expenses = float(expenses_result)
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0.0

    count_and_avg = db.execute(
        select(
            func.count(Transaction.id),
            func.coalesce(func.avg(Transaction.amount), 0),
        ).where(Transaction.user_id == user_id)
    ).one()

    transaction_count, avg_amount = count_and_avg

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate": round(savings_rate, 2),
        "average_transaction_amount": round(float(avg_amount), 2),
        "transaction_count": transaction_count,
    }
def get_category_breakdown(user_id: int, db: Session) -> list[dict]:
    rows = db.execute(
        select(
            Transaction.category,
            func.sum(Transaction.amount),
            func.count(Transaction.id),
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "debit",
        )
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
    ).all()

    total_expenses = sum(row[1] for row in rows) or 1

    return [
        {
            "category": row[0] or "Other",
            "total_amount": round(float(row[1]), 2),
            "percentage": round(float(row[1]) / total_expenses * 100, 2),
            "transaction_count": row[2],
        }
        for row in rows
    ]
def get_monthly_trend(user_id: int, db: Session) -> list[dict]:
    rows = db.execute(
        select(
            func.to_char(Transaction.transaction_date, "YYYY-MM").label("month"),
            Transaction.transaction_type,
            func.sum(Transaction.amount),
        )
        .where(Transaction.user_id == user_id)
        .group_by("month", Transaction.transaction_type)
        .order_by("month")
    ).all()

    monthly = {}
    for month, txn_type, total in rows:
        if month not in monthly:
            monthly[month] = {"income": 0.0, "expenses": 0.0}
        if txn_type == "credit":
            monthly[month]["income"] = float(total)
        else:
            monthly[month]["expenses"] = float(total)

    return [
        {
            "month": month,
            "income": round(data["income"], 2),
            "expenses": round(data["expenses"], 2),
            "net_savings": round(data["income"] - data["expenses"], 2),
        }
        for month, data in sorted(monthly.items())
    ]
def get_top_merchants(user_id: int, db: Session, limit: int = 10) -> list[dict]:
    rows = db.execute(
        select(
            Transaction.merchant,
            func.sum(Transaction.amount),
            func.count(Transaction.id),
        )
        .where(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "debit",
        )
        .group_by(Transaction.merchant)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(limit)
    ).all()

    return [
        {
            "merchant": row[0] or "Unknown",
            "total_amount": round(float(row[1]), 2),
            "transaction_count": row[2],
        }
        for row in rows
    ]