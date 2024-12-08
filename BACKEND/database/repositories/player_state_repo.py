from sqlalchemy.orm import Session
from datetime import datetime
from database.models.player_state import PlayerState
from database.models.game import Game
from database.repositories.game_medical_data_repo import get_game_medical_data_by_player_id
from database.repositories.player_device_at_repo import get_player_by_device_id
from database.repositories.heart_rate_data_repo import get_past_heart_rate_data_by_device_id

def new_player_state(session: Session, heart_rate: int, timestamp: datetime, game: Game, device_id: str) -> PlayerState | None:
    # Get the player
    player = get_player_by_device_id(session, device_id)

    # Get the player's medical data
    medical_data = get_game_medical_data_by_player_id(session, player.id)

    # Determine the player's state
    state = "Missing data"
    if heart_rate < medical_data.zone2_min_HR:
        state = "Ready"
    else:
        # We need the last heart rate data points to determine the player's state
        last_hr_data = get_past_heart_rate_data_by_device_id(session, device_id)
        last_hr_data_list = [hr_data.heart_rate for hr_data in last_hr_data]
        if heart_rate < medical_data.zone3_min_HR:
            if is_significantly_increasing(last_hr_data_list):
                state = "Active"
            else:
                state = "Recovering"
        else:
            # The user is in zone 3 - 5
            if is_significantly_decreasing(last_hr_data_list):
                state = "Recovering"
            else:
                state = "Active"

    # Determine the player's recovery score
    recovery_score = max(0, min(100, round(((medical_data.max_HR - heart_rate) / (medical_data.max_HR - medical_data.zone1_min_HR)) * 100)))

    # Create the new player state
    player_state = PlayerState(player=player, game=game, timestamp=timestamp, rec_score=recovery_score, state=state, heart_rate=heart_rate)
    session.add(player_state)
    session.commit()
    return player_state


def get_player_state_by_player_and_game_id(session: Session, player_id: int, game_id: int) -> PlayerState | None:
    player_state = session.query(PlayerState).filter(
        PlayerState.player_id == player_id,
        PlayerState.game_id == game_id
    ).order_by(PlayerState.timestamp.desc()).first()
    return player_state


def is_significantly_increasing(hr_data_list: list[int]) -> bool:
    if len(hr_data_list) < 2:
        return False
    # If the heart rate does not increase between the first element of the list (most recent)
    # and the last element of the list (oldest), return False
    if hr_data_list[0] - hr_data_list[-1] > 0:
        # if there is any decrease between consecutive heart rates, return False
        for i in range(1, len(hr_data_list)):
            if hr_data_list[i - 1] - hr_data_list[i] < 0:
                return False
        return True
    else:
        return False

def is_significantly_decreasing(hr_data_list: list[int]) -> bool:
    if len(hr_data_list) < 2:
        return False
    # If the heart rate does not decrease between the first element of the list (most recent)
    # and the last element of the list (oldest), return False
    if hr_data_list[0] - hr_data_list[-1] < 0:
        # if there is any increase between consecutive heart rates, return False
        for i in range(1, len(hr_data_list)):
            if hr_data_list[i - 1] - hr_data_list[i] > 0:
                return False
        return True
    else:
        return False