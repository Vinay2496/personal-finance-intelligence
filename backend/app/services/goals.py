from datetime import date
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.services.analytics import get_summary_kpis


def _months_between(today: date, deadline: date) -> int:
    months = (deadline.year - today.year) * 12 + (deadline.month - today.month)
    return max(months, 0)


def _build_goal_response(goal: Goal, current_savings: float, avg_monthly_savings: float) -> dict:
    today = date.today()
    months_remaining = _months_between(today, goal.deadline)

    remaining_amount = max(goal.target_amount - current_savings, 0)
    required_monthly_saving = (
        remaining_amount / months_remaining if months_remaining > 0 else remaining_amount
    )

    on_track = avg_monthly_savings >= required_monthly_saving if months_remaining > 0 else current_savings >= goal.target_amount

    return {
        "id": goal.id,
        "name": goal.name,
        "target_amount": goal.target_amount,
        "deadline": goal.deadline,
        "current_savings": round(current_savings, 2),
        "required_monthly_saving": round(required_monthly_saving, 2),
        "months_remaining": months_remaining,
        "on_track": on_track,
    }


def create_goal(user_id: int, name: str, target_amount: float, deadline: date, db: Session) -> dict:
    goal = Goal(user_id=user_id, name=name, target_amount=target_amount, deadline=deadline)
    db.add(goal)
    db.commit()
    db.refresh(goal)

    kpis = get_summary_kpis(user_id, db)
    return _build_goal_response(goal, kpis["net_savings"], kpis["net_savings"])


def list_goals(user_id: int, db: Session) -> list[dict]:
    goals = db.query(Goal).filter(Goal.user_id == user_id).order_by(Goal.deadline).all()
    kpis = get_summary_kpis(user_id, db)
    current_savings = kpis["net_savings"]

    return [_build_goal_response(g, current_savings, current_savings) for g in goals]


def delete_goal(user_id: int, goal_id: int, db: Session) -> bool:
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()
    if goal is None:
        return False
    db.delete(goal)
    db.commit()
    return True