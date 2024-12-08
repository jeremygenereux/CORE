# Repository for player table. Will define all the CRUD operations for this table.
import datetime
from sqlalchemy import Row, func
from sqlalchemy.orm import Session, joinedload

from database.models.player import Player
from database.models.line import Line
from database.repositories.game_medical_data_repo import get_most_recent_medical_data_sq
from database.repositories.player_device_at_repo import get_devices_of_all_players_sq

def get_players_by_team(session: Session, team_id: int) -> list[Row[tuple[Player, Line]]]:
    # Subquery to get the most recent device for each player and appending the latest timestamp the device was connected
    most_recent_devices_sq = get_devices_of_all_players_sq(session)

    # Subquery to get the most recent medical data for each player
    most_recent_medical_data_sq = get_most_recent_medical_data_sq(session)

    # Query to get all players from a team, including information about the line they are on, their device and medical data
    players = (
        session.query(Player, Line)
        .filter(Player.team_id == team_id)
        .outerjoin(Line)
        .outerjoin(most_recent_devices_sq, Player.id == most_recent_devices_sq.c.player_id)
        .outerjoin(most_recent_medical_data_sq, Player.id == most_recent_medical_data_sq.c.player_id)
        .add_columns(most_recent_devices_sq.c.device_id, most_recent_devices_sq.c.latest_timestamp, most_recent_medical_data_sq.c.max_HR, most_recent_medical_data_sq.c.rest_HR)
        .all()
    )
    return players

def create_player(session: Session, team_id: int, first_name: str, last_name: str, birth_date: datetime, email: str) -> Player:
    player = Player(team_id=team_id, first_name=first_name, last_name=last_name, birth_date=birth_date, email=email)
    session.add(player)
    session.commit()
    return player

def update_player(session: Session, player_id: int, first_name: str, last_name: str, birth_date: datetime, email: str, number: int | None, position: str | None) -> Player | None:
    player = session.query(Player).filter(Player.id == player_id).first()

    player.first_name = first_name
    player.last_name = last_name
    player.birth_date = birth_date
    player.email = email
    player.number = number
    player.position = position
    session.commit()

    return player

def get_player_by_id(session: Session, player_id: int) -> Player | None:
    return session.query(Player).filter(Player.id == player_id).first()

# Returns the players of a specified team that are on a line
def get_player_on_line_by_team_id(session: Session, team_id):
    players = session.query(Player).filter(Player.team_id == team_id, Player.line_id != None).join(Line).add_columns(Line.line_number, Line.is_offense).all()
    return players

def get_players_devices_on_team(session: Session, team_id: int) -> list[Row[tuple[Player, str]]]:
    # Subquery to get the most recent device for each player and appending the latest timestamp the device was connected
    most_recent_devices_sq = get_devices_of_all_players_sq(session)

    players = (
        session.query(Player)
        .filter(Player.team_id == team_id)
        .outerjoin(most_recent_devices_sq, Player.id == most_recent_devices_sq.c.player_id)
        .add_columns(most_recent_devices_sq.c.device_id)
        .all()
    )
    return players

# Returns the players of a specified team (used for the line endpoint)
def get_players_line(session: Session, team_id: int) -> list[type[Player]]:
    players = session.query(Player).filter(Player.team_id == team_id).all()
    return players

def remove_player_from_line(session: Session, player_id: int) -> Player | None:
    player = session.query(Player).filter(Player.id == player_id).first()
    player.line_id = None
    session.commit()
    return player

def add_player_to_line(session: Session, player_id: int, line_id: int) -> Player | None:
    player = session.query(Player).filter(Player.id == player_id).first()
    player.line_id = line_id
    session.commit()
    return player