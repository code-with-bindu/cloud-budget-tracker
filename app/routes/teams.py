from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Team
from app.schemas.schemas import TeamCreate, TeamResponse

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

# Create a team
@router.post("/", response_model=TeamResponse)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    existing_team = db.query(Team).filter(Team.name == team.name).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    
    new_team = Team(
        name=team.name,
        description=team.description
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


# Get all teams
@router.get("/", response_model=List[TeamResponse])
def get_all_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams


# Get single team
@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


# Delete a team
@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return {"message": f"Team {team.name} deleted successfully"}