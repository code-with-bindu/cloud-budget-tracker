from fastapi import FastAPI
from app.database import Base, engine
from app.routes import teams, expenses, budgets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Budget Tracker API",
    description="Track cloud spending across teams - Built for FinOps",
    version="1.0.0"
)

app.include_router(teams.router)
app.include_router(expenses.router)
app.include_router(budgets.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Cloud Budget Tracker API",
        "docs": "Go to /docs to see all APIs"
    }