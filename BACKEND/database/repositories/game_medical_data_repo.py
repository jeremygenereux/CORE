from datetime import datetime
from sqlalchemy.orm import Session
from database.models.game_medical_data import GameMedicalData
from sqlalchemy import func
from database.models.player import Player

def get_most_recent_medical_data_sq(session: Session):
    # Subquery to get the (player_id, timestamp) of the most recent medical data for each player
    player_ts_sq = (
        session.query(
            GameMedicalData.player_id,
            func.max(GameMedicalData.timestamp).label('latest_timestamp')
        )
        .group_by(GameMedicalData.player_id)
        .subquery()
    )

    # Subquery to get the most recent medical data for each player based on the previous subquery
    most_recent_medical_data_sq = (
        session.query(GameMedicalData)
        .join(player_ts_sq, (GameMedicalData.player_id == player_ts_sq.c.player_id) & (
                GameMedicalData.timestamp == player_ts_sq.c.latest_timestamp))
        .subquery()
    )
    return most_recent_medical_data_sq

def add_game_medical_data(session : Session, player_id: int, rest_HR: int, max_HR: int):
    player = session.query(Player).get(player_id)
    if player is None:
        return None
    ts_now = datetime.now()
    game_medical_data = GameMedicalData(player=player, timestamp=ts_now, rest_HR=rest_HR, max_HR=max_HR)
    session.add(game_medical_data)
    session.commit()
    return game_medical_data

def add_default_game_medical_data(session : Session, player_id: int):
    player = session.query(Player).get(player_id)
    if player is None:
        return None
    player_age = datetime.now().year - player.birth_date.year
    player_fc_max = GameMedicalData.calculate_max_HR(player_age)
    game_medical_data = GameMedicalData(player, datetime.now(), player_fc_max, 50)
    session.add(game_medical_data)
    session.commit()
    return game_medical_data

def get_game_medical_data_by_player_id(session: Session, player_id: int) -> GameMedicalData | None:
    return session.query(GameMedicalData).filter(GameMedicalData.player_id == player_id).order_by(GameMedicalData.timestamp.desc()).first()