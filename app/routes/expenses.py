from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Expense, Team
from app.schemas.schemas import ExpenseCreate, ExpenseResponse

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# Log an expense
@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == expense.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    new_expense = Expense(
        team_id=expense.team_id,
        service=expense.service,
        amount=expense.amount,
        description=expense.description
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


# Get all expenses
@router.get("/", response_model=List[ExpenseResponse])
def get_all_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    return expenses


# Get expenses by team
@router.get("/team/{team_id}", response_model=List[ExpenseResponse])
def get_team_expenses(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    expenses = db.query(Expense).filter(
        Expense.team_id == team_id
    ).all()
    return expenses


# Get expenses by service
@router.get("/service/{service_name}", response_model=List[ExpenseResponse])
def get_expenses_by_service(service_name: str, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(
        Expense.service == service_name
    ).all()
    return expenses


# Delete an expense
@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


# Monthly report
@router.get("/report/monthly")
def monthly_report(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()

    report = {}
    for expense in expenses:
        team_id = expense.team_id
        if team_id not in report:
            team = db.query(Team).filter(Team.id == team_id).first()
            report[team_id] = {
                "team_name": team.name,
                "total_spent": 0,
                "services": {}
            }
        report[team_id]["total_spent"] += expense.amount
        service = expense.service
        if service not in report[team_id]["services"]:
            report[team_id]["services"][service] = 0
        report[team_id]["services"][service] += expense.amount

    return report