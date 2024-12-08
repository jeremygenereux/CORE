
from sqlalchemy.orm import Session
from database.models.line import Line

def get_lines(session: Session, team_id: int) -> list[type[Line]]:
    lines = session.query(Line).filter(Line.team_id == team_id).all()
    return lines

def get_line_by_id(session: Session, line_id: int) -> Line | None:
    return session.query(Line).filter(Line.id == line_id).first()