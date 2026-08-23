import os
import shutil
import tempfile

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.transaction import UploadSummary
from app.services.auth_dependency import get_current_user
from app.services.transaction_import import (
    read_file_to_dataframe,
    detect_columns,
    clean_and_import,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])

ALLOWED_EXTENSIONS = {".csv", ".xls", ".xlsx"}


@router.post("/upload", response_model=UploadSummary)
def upload_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Please upload CSV or Excel.",
        )

    # Save uploaded file to a temporary location so pandas can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        df = read_file_to_dataframe(tmp_path, filename)

        if df.empty:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")

        columns = detect_columns(df)

        result = clean_and_import(
            df=df,
            columns=columns,
            user_id=current_user.id,
            source_file=filename,
            db=db,
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.remove(tmp_path)