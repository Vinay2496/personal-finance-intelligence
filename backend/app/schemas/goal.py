from datetime import date
from pydantic import BaseModel


class GoalCreate(BaseModel):
    name: str
    target_amount: float
    deadline: date


class GoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    deadline: date
    current_savings: float
    required_monthly_saving: float
    months_remaining: int
    on_track: bool

    class Config:
        from_attributes = True