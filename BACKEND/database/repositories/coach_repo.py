# Repository for coach table. Will define all the CRUD operations for this table.

from sqlalchemy.orm import Session
from database.models.coach import Coach

def get_coach_by_email(session: Session, email: str) -> Coach | None:
    return session.query(Coach).filter(Coach.email == email).first()

def get_coach_by_id(session: Session, id: int) -> Coach | None:
    return session.query(Coach).filter(Coach.id == id).first()

def create_coach(session: Session, first_name: str, last_name: str, email: str, password: str) -> Coach:
    coach = Coach(first_name=first_name, last_name=last_name, email=email, password=password)
    session.add(coach)
    session.commit()
    return coach