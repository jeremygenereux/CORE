"""
fichier : database1.py
auteur  : Jeremy Genereux - genj2110
          Benjamin Carignan - carb1101
date    : oct. 2024
projet  : CORE
description : Configuration de la connexion a la base de donnees.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
import random


class Database:
    Base = declarative_base()

    def __init__(self, user, password, host, port, db):
        self.user = user
        self.__password = password
        self.host = host
        self.port = port
        self.db = db
        self.engine = self.get_engine()
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        print("Database initialized")

    def get_engine(self):
        url = f"postgresql://{self.user}:{self.__password}@{self.host}:{self.port}/{self.db}"
        if not database_exists(url):
            create_database(url)
        return create_engine(url, pool_size=10, echo=False)

    def get_session(self):
        return Session(bind=self.engine)

    def create_tables(self):
        # Import models to register them with Base.metadata
        from .models import coach, player, team, game, line, heart_rate_data, device, game_medical_data, player_device_at, player_state

        # Create all tables
        self.Base.metadata.create_all(bind=self.engine)
        print("Tables created")

    def delete_tables(self):
        # Import models to register them with Base.metadata
        from .models import coach, player, team, game, line, heart_rate_data, device, game_medical_data, player_device_at, player_state

        # Drop all tables
        self.Base.metadata.drop_all(bind=self.engine)
        print("Tables dropped")

    def populate_tables(self):
        from database.models.device import Device
        from database.models.coach import Coach
        from database.models.team import Team
        from database.models.line import Line
        from database.models.player import Player
        from database.models.game import Game
        from database.models.game_medical_data import GameMedicalData
        from database.models.player_device_at import PlayerDeviceAt
        from database.models.heart_rate_data import HeartRateData
        from database.models.player_state import PlayerState


        # Create a session instance
        session = Session(bind=self.engine)

        with session.begin():
            # Create and add a coach
            coach = Coach(first_name="Martin", last_name="St-Louis", email="Martin.St-Louis@mtl.com", password="1234")
            session.add(coach)

            # Create and add a team
            team = Team(team_name="Montreal Canadiens", coach=coach, primary_color="#FF0000", secondary_color="#0000FF")
            session.add(team)

            # Create and add devices
            devices = [Device(id=f"552-{i}", brand="Polar", model="H10") for i in range(1, 26)]
            for device in devices:
                session.add(device)


            # Create and add lines
            offLine1 = Line(team=team, line_number=1, is_offense=True)
            offLine2 = Line(team=team, line_number=2, is_offense=True)
            offLine3 = Line(team=team, line_number=3, is_offense=True)
            offLine4 = Line(team=team, line_number=4, is_offense=True)
            session.add(offLine1)
            session.add(offLine2)
            session.add(offLine3)
            session.add(offLine4)

            defLine1 = Line(team=team, line_number=1, is_offense=False)
            defLine2 = Line(team=team, line_number=2, is_offense=False)
            defLine3 = Line(team=team, line_number=3, is_offense=False)
            session.add(defLine1)
            session.add(defLine2)
            session.add(defLine3)

            # Create and add players
            players = [
                Player(first_name="Nick", last_name="Suzuki", birth_date=datetime.strptime("1999-08-10", "%Y-%m-%d"),
                       position="Center", number=14, team=team, line=offLine1),
                Player(first_name="Cole", last_name="Caufield", birth_date=datetime.strptime("2001-01-02", "%Y-%m-%d"),
                       position="Left Wing", number=13, team=team, line=offLine1),
                Player(first_name="Kirby", last_name="Dach", birth_date=datetime.strptime("2001-01-21", "%Y-%m-%d"),
                       position="Right Wing", number=77, team=team, line=offLine1),
                Player(first_name="Joel", last_name="Armia", birth_date=datetime.strptime("1993-05-31", "%Y-%m-%d"),
                       position="Right Wing", number=40, team=team, line=offLine2),
                Player(first_name="Alex", last_name="Newhook", birth_date=datetime.strptime("1996-07-28", "%Y-%m-%d"),
                       position="Center", number=15, team=team, line=offLine2),
                Player(first_name="Juraj", last_name="Slafkovsky",
                       birth_date=datetime.strptime("2003-09-07", "%Y-%m-%d"), position="Left Wing", number=20,
                       team=team, line=offLine2),
                Player(first_name="Josh", last_name="Anderson", birth_date=datetime.strptime("1994-05-07", "%Y-%m-%d"),
                       position="Right Wing", number=17, team=team, line=offLine3),
                Player(first_name="Brendan", last_name="Gallagher",
                       birth_date=datetime.strptime("1992-05-06", "%Y-%m-%d"), position="Left Wing", number=11,
                       team=team, line=offLine3),
                Player(first_name="Jake", last_name="Evans", birth_date=datetime.strptime("1996-06-02", "%Y-%m-%d"),
                       position="Center", number=71, team=team, line=offLine3),
                Player(first_name="Olivier", last_name="Kapanen",
                       birth_date=datetime.strptime("1996-07-28", "%Y-%m-%d"), position="Left Wing", number=91,
                       team=team, line=offLine4),
                Player(first_name="Christian", last_name="Dvorak",
                       birth_date=datetime.strptime("1996-02-02", "%Y-%m-%d"), position="Center", number=28, team=team,
                       line=offLine4),
                Player(first_name="Emil", last_name="Heineman", birth_date=datetime.strptime("2003-02-16", "%Y-%m-%d"),
                       position="Right Wing", number=51, team=team, line=offLine4),
                Player(first_name="Mike", last_name="Matheson", birth_date=datetime.strptime("1994-02-27", "%Y-%m-%d"),
                       position="Defensemen", number=5, team=team, line=defLine1),
                Player(first_name="Jayden", last_name="Struble", birth_date=datetime.strptime("2002-09-08", "%Y-%m-%d"),
                       position="Defensemen", number=47, team=team, line=defLine1),
                Player(first_name="Lane", last_name="Hutson", birth_date=datetime.strptime("2003-04-12", "%Y-%m-%d"),
                       position="Defensemen", number=48, team=team, line=defLine2),
                Player(first_name="David", last_name="Savard", birth_date=datetime.strptime("1990-10-22", "%Y-%m-%d"),
                       position="Defensemen", number=58, team=team, line=defLine2),
                Player(first_name="Arber", last_name="Xhekaj", birth_date=datetime.strptime("2003-01-01", "%Y-%m-%d"),
                       position="Defensemen", number=72, team=team, line=defLine3),
                Player(first_name="Logan", last_name="Mailloux", birth_date=datetime.strptime("2003-04-15", "%Y-%m-%d"),
                       position="Defensemen", number=24, team=team, line=defLine3),
                Player(first_name="Kaiden", last_name="Guhle", birth_date=datetime.strptime("2002-01-18", "%Y-%m-%d"),
                       position="Defensemen", number=22, team=team),
                Player(first_name="Patrik", last_name="Laine", birth_date=datetime.strptime("1998-04-19", "%Y-%m-%d"),
                       position="Right Wing", number=29, team=team),
            ]
            for player in players:
                session.add(player)

            # Create and add games
            games = [
                Game(team=team, start_ts=datetime.strptime("2024-10-01 19:00:00", "%Y-%m-%d %H:%M:%S"),
                     end_ts=datetime.strptime("2024-10-01 21:30:00", "%Y-%m-%d %H:%M:%S"), is_underway=False),
                Game(team=team, start_ts=datetime.strptime("2024-10-03 19:00:00", "%Y-%m-%d %H:%M:%S"),
                     end_ts=datetime.strptime("2024-10-03 21:30:00", "%Y-%m-%d %H:%M:%S"), is_underway=False),
                Game(team=team, start_ts=datetime.strptime("2024-10-05 19:00:00", "%Y-%m-%d %H:%M:%S"),
                     end_ts=datetime.strptime("2024-10-05 21:30:00", "%Y-%m-%d %H:%M:%S"), is_underway=False),
                Game(team=team, start_ts=datetime.strptime("2024-10-07 19:00:00", "%Y-%m-%d %H:%M:%S"), is_underway=True)
            ]
            for game in games:
                session.add(game)

            # Create and add game medical data
            for player in players:
                player_age = datetime.now().year - player.birth_date.year
                player_fc_max = GameMedicalData.calculate_max_HR(player_age)
                game_medical_data = GameMedicalData(player, datetime.now(), player_fc_max, random.randint(40, 70))
                session.add(game_medical_data)

            # Create and add current player devices
            for i in range(len(players)-1):
                current_player_device = PlayerDeviceAt(device=devices[i], player=players[i], timestamp=datetime.now())
                session.add(current_player_device)

            # Create and add heart rate data
            for device in devices:
                for i in range(10):
                    heart_rate_data = HeartRateData(device=device, game=games[3], timestamp=datetime.now(), heart_rate=random.randint(70, 170))
                    session.add(heart_rate_data)

            # Create and add player states
            for player in players:
                for i in range(10):
                    stateNumber = random.randint(0, 2)
                    state = ["resting", "active", "recovery"]
                    rec_score = random.randint(0, 100)
                    heart_rate = random.randint(70, 180)
                    player_state = PlayerState(player=player, game=games[3], state=state[stateNumber], rec_score=rec_score, timestamp=datetime.now(), heart_rate=heart_rate)
                    session.add(player_state)

        print("Tables populated")

