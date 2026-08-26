from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.forecast import ForecastResult
from app.services.auth_dependency import get_current_user
from app.services.forecasting import get_spending_forecast

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("", response_model=ForecastResult)
def forecast(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_spending_forecast(current_user.id, db)