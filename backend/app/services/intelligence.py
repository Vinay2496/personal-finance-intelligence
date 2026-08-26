from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from statistics import mean, stdev

from app.models.transaction import Transaction


def _get_month_str(d: date) -> str:
    return d.strftime("%Y-%m")


def get_month_comparison(user_id: int, db: Session) -> dict | None:
    rows = db.execute(
        select(
            func.to_char(Transaction.transaction_date, "YYYY-MM").label("month"),
            func.sum(Transaction.amount),
        )
        .where(Transaction.user_id == user_id, Transaction.transaction_type == "debit")
        .group_by("month")
        .order_by("month")
    ).all()

    if not rows:
        return None

    months = {row[0]: float(row[1]) for row in rows}
    sorted_months = sorted(months.keys())

    current_month = sorted_months[-1]
    current_expenses = months[current_month]

    if len(sorted_months) < 2:
        return {
            "current_month": current_month,
            "previous_month": None,
            "current_expenses": round(current_expenses, 2),
            "previous_expenses": None,
            "change_amount": None,
            "change_percent": None,
        }

    previous_month = sorted_months[-2]
    previous_expenses = months[previous_month]
    change_amount = current_expenses - previous_expenses
    change_percent = (
        (change_amount / previous_expenses * 100) if previous_expenses > 0 else 0.0
    )

    return {
        "current_month": current_month,
        "previous_month": previous_month,
        "current_expenses": round(current_expenses, 2),
        "previous_expenses": round(previous_expenses, 2),
        "change_amount": round(change_amount, 2),
        "change_percent": round(change_percent, 2),
    }


def get_category_changes(user_id: int, db: Session) -> list[dict]:
    rows = db.execute(
        select(
            func.to_char(Transaction.transaction_date, "YYYY-MM").label("month"),
            Transaction.category,
            func.sum(Transaction.amount),
        )
        .where(Transaction.user_id == user_id, Transaction.transaction_type == "debit")
        .group_by("month", Transaction.category)
        .order_by("month")
    ).all()

    if not rows:
        return []

    months = sorted(set(row[0] for row in rows))
    if len(months) < 2:
        return []

    current_month, previous_month = months[-1], months[-2]

    current_by_cat = {
        row[1]: float(row[2]) for row in rows if row[0] == current_month
    }
    previous_by_cat = {
        row[1]: float(row[2]) for row in rows if row[0] == previous_month
    }

    all_categories = set(current_by_cat) | set(previous_by_cat)

    changes = []
    for cat in all_categories:
        current_amt = current_by_cat.get(cat, 0.0)
        previous_amt = previous_by_cat.get(cat, 0.0)
        change = current_amt - previous_amt
        if abs(change) > 0.01:
            changes.append({
                "category": cat or "Other",
                "current_amount": round(current_amt, 2),
                "previous_amount": round(previous_amt, 2),
                "change_amount": round(change, 2),
            })

    changes.sort(key=lambda x: abs(x["change_amount"]), reverse=True)
    return changes
def get_recurring_expenses(user_id: int, db: Session, min_occurrences: int = 2) -> list[dict]:
    rows = db.execute(
        select(Transaction.merchant, Transaction.amount, Transaction.transaction_date)
        .where(Transaction.user_id == user_id, Transaction.transaction_type == "debit")
    ).all()

    from collections import defaultdict
    merchant_data = defaultdict(list)
    for merchant, amount, txn_date in rows:
        if merchant:
            merchant_data[merchant].append((float(amount), txn_date))

    recurring = []
    for merchant, entries in merchant_data.items():
        if len(entries) < min_occurrences:
            continue

        amounts = [e[0] for e in entries]
        avg_amount = mean(amounts)

        # Consider "recurring" if amounts are consistent (low variance) across multiple months
        months_seen = set(_get_month_str(e[1]) for e in entries)
        if len(months_seen) >= min_occurrences:
            recurring.append({
                "merchant": merchant,
                "average_amount": round(avg_amount, 2),
                "occurrence_count": len(entries),
                "frequency": "monthly",
            })

    recurring.sort(key=lambda x: x["average_amount"], reverse=True)
    return recurring


def get_unusual_transactions(user_id: int, db: Session, z_threshold: float = 2.0) -> list[dict]:
    rows = db.execute(
        select(Transaction)
        .where(Transaction.user_id == user_id, Transaction.transaction_type == "debit")
    ).scalars().all()

    if len(rows) < 5:
        return []

    amounts = [t.amount for t in rows]
    avg = mean(amounts)
    try:
        std = stdev(amounts)
    except Exception:
        std = 0

    if std == 0:
        return []

    unusual = []
    for txn in rows:
        z_score = (txn.amount - avg) / std
        if z_score > z_threshold:
            unusual.append({
                "id": txn.id,
                "description": txn.description,
                "merchant": txn.merchant,
                "amount": txn.amount,
                "transaction_date": txn.transaction_date.isoformat(),
                "reason": f"This transaction is significantly larger than your typical spending (₹{avg:.0f} average).",
            })

    unusual.sort(key=lambda x: x["amount"], reverse=True)
    return unusual
def generate_insights(user_id: int, db: Session) -> dict:
    month_comp = get_month_comparison(user_id, db)
    category_changes = get_category_changes(user_id, db)
    recurring = get_recurring_expenses(user_id, db)
    unusual = get_unusual_transactions(user_id, db)

    insights = []

    if month_comp and month_comp["change_percent"] is not None:
        pct = month_comp["change_percent"]
        if pct > 5:
            insights.append({
                "type": "spending_increase",
                "message": f"Your spending increased {pct:.1f}% compared with last month.",
            })
        elif pct < -5:
            insights.append({
                "type": "spending_decrease",
                "message": f"Your spending decreased {abs(pct):.1f}% compared with last month.",
            })

    for change in category_changes[:3]:
        if change["change_amount"] > 0:
            insights.append({
                "type": "category_increase",
                "message": f"{change['category']} spending increased by ₹{change['change_amount']:.0f} compared with last month.",
            })

    if recurring:
        total_recurring = sum(r["average_amount"] for r in recurring)
        insights.append({
            "type": "recurring",
            "message": f"You have {len(recurring)} recurring expense(s) costing approximately ₹{total_recurring:.0f}/month.",
        })

    if unusual:
        insights.append({
            "type": "unusual",
            "message": f"{len(unusual)} unusual transaction(s) detected that are significantly larger than your typical spending.",
        })

    return {
        "insights": insights,
        "month_comparison": month_comp,
        "category_changes": category_changes,
        "recurring_expenses": recurring,
        "unusual_transactions": unusual,
    }