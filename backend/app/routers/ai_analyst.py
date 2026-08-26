from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.ai_analyst import AskRequest, AskResponse
from app.services.auth_dependency import get_current_user
from app.services.ai_analyst import ask_ai_analyst

router = APIRouter(prefix="/ai-analyst", tags=["ai-analyst"])


@router.post("/ask", response_model=AskResponse)
def ask(
    request: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = ask_ai_analyst(request.question, current_user.id, db)
    return {"answer": answer}