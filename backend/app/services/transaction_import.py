import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.transaction import Transaction
from app.services.categorization import categorize_transaction


DATE_COLUMNS = ["date", "transaction date", "txn date", "value date"]
DESCRIPTION_COLUMNS = ["description", "narration", "transaction details", "remarks"]
AMOUNT_COLUMNS = ["amount"]
TYPE_COLUMNS = ["type", "transaction type", "debit/credit"]


def _normalize_column_name(col: str) -> str:
    return col.strip().lower()


def _find_column(columns: list[str], candidates: list[str]) -> str | None:
    normalized = {_normalize_column_name(c): c for c in columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


def read_file_to_dataframe(file_path: str, filename: str) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        return pd.read_csv(file_path)
    elif filename.lower().endswith((".xls", ".xlsx")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a CSV or Excel file.")


def detect_columns(df: pd.DataFrame) -> dict:
    columns = list(df.columns)

    date_col = _find_column(columns, DATE_COLUMNS)
    desc_col = _find_column(columns, DESCRIPTION_COLUMNS)
    amount_col = _find_column(columns, AMOUNT_COLUMNS)
    type_col = _find_column(columns, TYPE_COLUMNS)

    missing = []
    if not date_col:
        missing.append("date")
    if not desc_col:
        missing.append("description")
    if not amount_col:
        missing.append("amount")

    if missing:
        raise ValueError(f"Could not detect required column(s): {', '.join(missing)}")

    return {
        "date": date_col,
        "description": desc_col,
        "amount": amount_col,
        "type": type_col,
    }


def extract_merchant(description: str) -> str:
    return description.strip().split()[0] if description.strip() else "Unknown"


def clean_and_import(
    df: pd.DataFrame,
    columns: dict,
    user_id: int,
    source_file: str,
    db: Session,
) -> dict:
    total_rows = len(df)
    inserted = 0
    duplicates_skipped = 0
    invalid_rows = 0
    errors = []

    existing = db.execute(
        select(
            Transaction.transaction_date,
            Transaction.description,
            Transaction.amount,
        ).where(Transaction.user_id == user_id)
    ).all()
    existing_keys = {(row[0], row[1].strip().lower(), round(row[2], 2)) for row in existing}

    new_transactions = []

    for idx, row in df.iterrows():
        row_num = idx + 2

        try:
            raw_date = row[columns["date"]]
            raw_description = row[columns["description"]]
            raw_amount = row[columns["amount"]]

            if pd.isna(raw_date) or pd.isna(raw_description) or pd.isna(raw_amount):
                invalid_rows += 1
                errors.append(f"Row {row_num}: missing required value(s), skipped.")
                continue

            parsed_date = pd.to_datetime(raw_date, errors="coerce")
            if pd.isna(parsed_date):
                invalid_rows += 1
                errors.append(f"Row {row_num}: could not parse date '{raw_date}', skipped.")
                continue
            parsed_date = parsed_date.date()

            try:
                amount = float(raw_amount)
            except (ValueError, TypeError):
                invalid_rows += 1
                errors.append(f"Row {row_num}: invalid amount '{raw_amount}', skipped.")
                continue

            description = str(raw_description).strip()

            if columns["type"]:
                raw_type = str(row[columns["type"]]).strip().lower()
                transaction_type = "credit" if "cred" in raw_type else "debit"
            else:
                transaction_type = "credit" if amount > 0 else "debit"

            amount = abs(amount)

            dedup_key = (parsed_date, description.strip().lower(), round(amount, 2))
            if dedup_key in existing_keys:
                duplicates_skipped += 1
                continue

            merchant = extract_merchant(description)
            category = categorize_transaction(description, merchant, transaction_type)

            new_transactions.append(
                Transaction(
                    user_id=user_id,
                    transaction_date=parsed_date,
                    description=description,
                    merchant=merchant,
                    amount=amount,
                    transaction_type=transaction_type,
                    category=category,
                    source_file=source_file,
                )
            )
            existing_keys.add(dedup_key)

        except Exception as e:
            invalid_rows += 1
            errors.append(f"Row {row_num}: unexpected error ({str(e)}), skipped.")
            continue

    if new_transactions:
        db.add_all(new_transactions)
        db.commit()
        inserted = len(new_transactions)

    return {
        "total_rows": total_rows,
        "inserted": inserted,
        "duplicates_skipped": duplicates_skipped,
        "invalid_rows": invalid_rows,
        "errors": errors[:20],
    }