from pydantic import BaseModel
from typing import Optional


class ForecastResult(BaseModel):
    forecast_month: Optional[str] = None
    predicted_expenses: Optional[float] = None
    method_used: Optional[str] = None
    reliable: bool
    reliability_note: str
    mae: Optional[float] = None
    historical_months_used: int