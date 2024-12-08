import sys
import os
from dotenv import load_dotenv
from .database import Database

# Import all models to ensure they are loaded and registered with the database
from database.models.team import Team
from database.models.game import Game
from database.models.player import Player
from database.models.line import Line
from database.models.game_medical_data import GameMedicalData
from database.models.player_device_at import PlayerDeviceAt
from database.models.player_state import PlayerState
from database.models.heart_rate_data import HeartRateData
from database.models.device import Device


def is_running_in_venv():
    return sys.prefix != getattr(sys, 'base_prefix', sys.prefix)


def main():
    if not is_running_in_venv():
        print("Not running inside a virtual environment.")
        raise EnvironmentError("The program must be run inside a virtual environment.")

    database = create_database()
    database.delete_tables()
    database.create_tables()
    database.populate_tables()

def create_database():
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    if not user or not password or not host or not port or not db:
        raise EnvironmentError("Missing environment variables for database1 connection.")

    return Database(user, password, host, port, db)

if __name__ == "__main__":
    main()
