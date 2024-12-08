from datetime import datetime
from sqlalchemy import desc, func, Subquery
from sqlalchemy.orm import Session
from database.models.player_device_at import PlayerDeviceAt
from database.models.player import Player
from database.models.device import Device
from database.repositories.device_repo import get_last_connection_devices_sq


def add_player_device_at(session : Session, player_id: int, device_id: str):
    player = session.query(Player).get(player_id)
    device = session.query(Device).get(device_id)
    if player is None or device is None:
        return None
    ts_now = datetime.now()
    player_device_at = PlayerDeviceAt(player=player, timestamp=ts_now, device=device)
    session.add(player_device_at)
    session.commit()
    return player_device_at

def get_player_by_device_id(session: Session, device_id: str) -> Player | None:
    from database.repositories.player_repo import get_player_by_id
    player_device_at = session.query(PlayerDeviceAt).filter(PlayerDeviceAt.device_id == device_id).order_by(desc(PlayerDeviceAt.timestamp)).first()
    if player_device_at is None:
        return None
    player = get_player_by_id(session, player_device_at.player_id)
    return player

def get_devices_of_all_players_sq(session: Session) -> Subquery:
    # Subquery that contains the last time each device was connected
    devices_last_conn_sq = get_last_connection_devices_sq(session)

    # Subquery to get the (player_id, timestamp) of the most recent device for each player
    player_ts_sq = (
        session.query(
            PlayerDeviceAt.player_id,
            func.max(PlayerDeviceAt.timestamp).label('latest_timestamp')
        )
        .group_by(PlayerDeviceAt.player_id)
        .subquery()
    )

    most_recent_devices_sq = (
        session.query(PlayerDeviceAt)
        .join(player_ts_sq, (PlayerDeviceAt.player_id == player_ts_sq.c.player_id) & (
                PlayerDeviceAt.timestamp == player_ts_sq.c.latest_timestamp))
        .outerjoin(devices_last_conn_sq, PlayerDeviceAt.device_id == devices_last_conn_sq.c.device_id)
        .add_columns(devices_last_conn_sq.c.latest_timestamp)
        .subquery()
    )

    return most_recent_devices_sq