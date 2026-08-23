from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.analytics import SummaryKPIs, CategoryBreakdownItem, MonthlyTrendItem, TopMerchantItem
from app.services.auth_dependency import get_current_user
from app.services.analytics import get_summary_kpis, get_category_breakdown, get_monthly_trend, get_top_merchants
router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryKPIs)
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_summary_kpis(current_user.id, db)
@router.get("/category-breakdown", response_model=list[CategoryBreakdownItem])
def category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_category_breakdown(current_user.id, db)
@router.get("/monthly-trend", response_model=list[MonthlyTrendItem])
def monthly_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_monthly_trend(current_user.id, db)
@router.get("/top-merchants", response_model=list[TopMerchantItem])
def top_merchants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_top_merchants(current_user.id, db)