from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Budget, Expense, Team
from app.schemas.schemas import BudgetCreate, BudgetResponse, BudgetStatus

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

# Create a budget
@router.post("/", response_model=BudgetResponse)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == budget.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    existing_budget = db.query(Budget).filter(
        Budget.team_id == budget.team_id,
        Budget.month == budget.month
    ).first()
    if existing_budget:
        raise HTTPException(status_code=400, detail="Budget already exists for this team and month")

    new_budget = Budget(
        team_id=budget.team_id,
        month=budget.month,
        amount=budget.amount
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget


# Get all budgets
@router.get("/", response_model=List[BudgetResponse])
def get_all_budgets(db: Session = Depends(get_db)):
    budgets = db.query(Budget).all()
    return budgets


# Get budget status for a team
@router.get("/status/{team_id}/{month}", response_model=BudgetStatus)
def get_budget_status(team_id: int, month: str, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    budget = db.query(Budget).filter(
        Budget.team_id == team_id,
        Budget.month == month
    ).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found for this month")

    expenses = db.query(Expense).filter(
        Expense.team_id == team_id
    ).all()

    total_spent = sum(e.amount for e in expenses)
    remaining = budget.amount - total_spent

    if remaining < 0:
        status = "EXCEEDED"
    elif remaining < budget.amount * 0.2:
        status = "WARNING"
    else:
        status = "SAFE"

    return BudgetStatus(
        team_name=team.name,
        month=month,
        total_budget=budget.amount,
        total_spent=total_spent,
        remaining=remaining,
        status=status
    )