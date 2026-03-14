# Cloud Budget Tracker API 🌐

A FinOps-inspired REST API built with **FastAPI** and **PostgreSQL** to track cloud spending across teams — similar to what platforms like Astuto OneLens do.

## 🚀 Features
- Create and manage teams (Backend, DevOps, Data etc)
- Set monthly cloud budgets per team
- Log cloud expenses per service (EC2, S3, Kubernetes etc)
- Auto budget status — SAFE / WARNING / EXCEEDED
- Monthly spending report by team and service

## 🛠️ Tech Stack
- **FastAPI** — REST API framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM for database models
- **Pydantic** — Data validation
- **Uvicorn** — ASGI server

## 📦 Installation
```bash
# Clone the repo
git clone https://github.com/code-with-bindu/cloud-budget-tracker

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv

# Run the server
uvicorn main:app --reload
```

## �API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /teams/ | Create a team |
| GET | /teams/ | Get all teams |
| GET | /teams/{id} | Get single team |
| DELETE | /teams/{id} | Delete a team |
| POST | /budgets/ | Set team budget |
| GET | /budgets/status/{team_id}/{month} | Get budget status |
| POST | /expenses/ | Log an expense |
| GET | /expenses/team/{team_id} | Get team expenses |
| GET | /expenses/report/monthly | Full monthly report |

## 🌐 API Docs
Run the server and visit:
```
http://127.0.0.1:8000/docs
```