#
from sqlalchemy.orm import Session
from database.models.team import Team

def get_teams_by_coach_id(session: Session, coach_id: int) -> list[Team]:
    return session.query(Team).filter(Team.coach_id == coach_id).all()

def create_team(session: Session, coach_id: int, team_name: str, primary_color: str, secondary_color: str) -> Team:
    team = Team(coach_id=coach_id, team_name=team_name, primary_color=primary_color, secondary_color=secondary_color)
    session.add(team)
    session.commit()
    return team