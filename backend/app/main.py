from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine, Base
from app.models import user, transaction
from app.routers import auth, transactions, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Personal Finance Intelligence API is running"}


@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "connection failed", "error": str(e)}