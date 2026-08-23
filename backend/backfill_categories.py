"""
One-off script to backfill categories for transactions that don't have one yet.
Run once with: python backfill_categories.py
"""
from app.database import SessionLocal
from app.models.transaction import Transaction
from app.models.user import User
from app.services.categorization import categorize_transaction
from sqlalchemy import select, or_

db = SessionLocal()

uncategorized = db.execute(
    select(Transaction).where(
        or_(Transaction.category.is_(None), Transaction.category == "")
    )
).scalars().all()

print(f"Found {len(uncategorized)} uncategorized transactions.")

for txn in uncategorized:
    new_category = categorize_transaction(txn.description, txn.merchant or "", txn.transaction_type)
    print(f"  #{txn.id} '{txn.description}' -> {new_category}")
    txn.category = new_category

db.commit()
db.close()

print("Backfill complete.")
