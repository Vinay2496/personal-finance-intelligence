from datetime import date, timedelta
from app.services.goals import _months_between, _build_goal_response
from app.models.goal import Goal


def test_months_between_basic():
    today = date(2026, 8, 27)
    deadline = date(2027, 6, 1)
    assert _months_between(today, deadline) == 10


def test_months_between_same_month():
    today = date(2026, 8, 27)
    deadline = date(2026, 8, 1)
    assert _months_between(today, deadline) == 0


def test_months_between_past_deadline_clamped_to_zero():
    today = date(2026, 8, 27)
    deadline = date(2025, 1, 1)
    assert _months_between(today, deadline) == 0


def _make_goal(target_amount: float, deadline: date) -> Goal:
    goal = Goal()
    goal.id = 1
    goal.name = "Test Goal"
    goal.target_amount = target_amount
    goal.deadline = deadline
    return goal


def test_goal_on_track_when_savings_exceed_target():
    goal = _make_goal(50000, date.today() + timedelta(days=300))
    result = _build_goal_response(goal, current_savings=133014, avg_monthly_savings=133014)
    assert result["on_track"] is True
    assert result["required_monthly_saving"] == 0


def test_goal_not_on_track_when_unrealistic():
    goal = _make_goal(5000000, date.today() + timedelta(days=120))
    result = _build_goal_response(goal, current_savings=133014, avg_monthly_savings=133014)
    assert result["on_track"] is False
    assert result["required_monthly_saving"] > 0


def test_goal_deadline_already_passed_uses_current_savings():
    goal = _make_goal(50000, date.today() - timedelta(days=10))
    result = _build_goal_response(goal, current_savings=60000, avg_monthly_savings=0)
    assert result["months_remaining"] == 0
    assert result["on_track"] is True