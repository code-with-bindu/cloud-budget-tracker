from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Team schemas
class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TeamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Budget schemas
class BudgetCreate(BaseModel):
    team_id: int
    month: str
    amount: float

class BudgetResponse(BaseModel):
    id: int
    team_id: int
    month: str
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True


# Expense schemas
class ExpenseCreate(BaseModel):
    team_id: int
    service: str
    amount: float
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    team_id: int
    service: str
    amount: float
    description: Optional[str] = None
    date: datetime

    class Config:
        from_attributes = True


# Budget status schema
class BudgetStatus(BaseModel):
    team_name: str
    month: str
    total_budget: float
    total_spent: float
    remaining: float
    status: str