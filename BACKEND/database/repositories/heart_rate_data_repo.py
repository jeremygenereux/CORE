from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import desc
from database.models.heart_rate_data import HeartRateData
from database.repositories.game_repo import get_team_current_game
from database.repositories.device_repo import get_device_by_id
from typing import Type


def new_heart_rate_data(session: Session, device_id: str, heart_rate: int, team_id: int) -> HeartRateData:
    ts_now = datetime.now()

    # Get the current game
    game = get_team_current_game(session, team_id)

    # Get the device
    device = get_device_by_id(session, device_id)

    # Create the new heart rate data
    heart_rate_data = HeartRateData(game=game, device=device, timestamp=ts_now, heart_rate=heart_rate)
    session.add(heart_rate_data)
    session.commit()
    return heart_rate_data

def get_past_heart_rate_data_by_device_id(session: Session, device_id: str) -> list[Type[HeartRateData]]:
    return session.query(HeartRateData).filter(HeartRateData.device_id == device_id).order_by(desc(HeartRateData.timestamp)).limit(5).all()