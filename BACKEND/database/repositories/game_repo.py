from sqlalchemy import desc
from sqlalchemy.orm import Session
from database.models.game import Game

def get_team_current_game(session: Session, team_id) -> Game | None:
    # Return the game underway (most recent if multiple)
    return session.query(Game).filter(Game.is_underway == True, Game.team_id == team_id).order_by(desc(Game.start_ts)).first()
