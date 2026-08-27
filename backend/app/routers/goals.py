from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalResponse
from app.services.auth_dependency import get_current_user
from app.services.goals import create_goal, list_goals, delete_goal

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalResponse)
def create(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_goal(current_user.id, goal.name, goal.target_amount, goal.deadline, db)


@router.get("", response_model=list[GoalResponse])
def list_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_goals(current_user.id, db)


@router.delete("/{goal_id}")
def delete(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = delete_goal(current_user.id, goal_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal deleted"}