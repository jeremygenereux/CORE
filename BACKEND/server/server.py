from random import randint

from fastapi import FastAPI, Query, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from database.repositories.player_state_repo import new_player_state
from server.auth_utils import create_access_token, check_password
from database.create_database import create_database
from database.repositories.coach_repo import get_coach_by_email, create_coach, get_coach_by_id
from database.repositories.team_repo import get_teams_by_coach_id, create_team
from database.repositories.player_repo import get_players_by_team, create_player, update_player, get_player_on_line_by_team_id, get_players_devices_on_team, get_players_line, remove_player_from_line, add_player_to_line
from database.repositories.game_medical_data_repo import add_game_medical_data, add_default_game_medical_data
from database.repositories.player_device_at_repo import add_player_device_at
from database.repositories.heart_rate_data_repo import new_heart_rate_data
from database.repositories.game_repo import get_team_current_game
from database.repositories.player_state_repo import get_player_state_by_player_and_game_id
from database.repositories.line_repo import get_lines, get_line_by_id
from server.websocket import WebsocketConnectionManager
import argparse
import asyncio
from contextlib import asynccontextmanager

print("Parsing arguments...")
parser = argparse.ArgumentParser(description="Launch the server with specified arguments.")
parser.add_argument('--data', type=bool, default=False, help='With or without fake data generation')
args = parser.parse_args()

stop_event = asyncio.Event()
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    stop_event.set()

print("Starting server...")
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Connecting to database...")
db = create_database()
session = db.get_session()
print("Starting websocket manager...")
websocket_manager = WebsocketConnectionManager()

# Global dictionary to hold the background tasks
background_tasks: dict[str, asyncio.Task] = {}

async def generate_hr_data(device_id: str, team_id: int):
    hr = randint(120, 175)
    increasing = True
    while not stop_event.is_set():
        await asyncio.sleep(3)
        print(f"Heart rate: {hr} bpm")
        increment = randint(0, 4)
        if increasing:
            hr += increment
            if hr >= 180:
                increasing = False
        else:
            hr -= increment
            if hr <= 120:
                increasing = True
        heart_rate_data = new_heart_rate_data(session=session, device_id=device_id, heart_rate=hr, team_id=team_id)
        player_state = new_player_state(session=session, heart_rate=hr, timestamp=heart_rate_data.timestamp, game=heart_rate_data.game, device_id=device_id)

        data = {
            "id": player_state.id,
            "playerId": player_state.player_id,
            "hr": heart_rate_data.heart_rate,
            "state": player_state.state,
            "recScore": player_state.rec_score,
            "timestamp": player_state.timestamp.isoformat(),
            "gameId": player_state.game_id
        }
        await websocket_manager.send_message(data)

def start_server():
    import uvicorn
    uvicorn.run("server.server:app", host='127.0.0.1', port=5000, reload=True)

# Endpoint to login a coach
class UserLogin(BaseModel):
    email: str
    password: str

class Coach(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    access_token: str

@app.post("/login", response_model=Coach)
async def login(user_login: UserLogin):
    # Fetch the user from the database
    user = get_coach_by_email(session, user_login.email)

    # Verify password
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not check_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }


# Endpoint to register a new coach
class UserRegister(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_register: UserRegister):
    # Fetch the user from the database
    user = get_coach_by_email(session, user_register.email)

    # Verify if user already exists
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        # Create the coach
        create_coach(session, user_register.first_name, user_register.last_name, user_register.email, user_register.password)
    return

# Endpoint to get the list of teams
class Team(BaseModel):
    id: int
    coach_id: int
    team_name: str
    primary_color: str
    secondary_color: str
    logo: Optional[str]
    description: Optional[str]
@app.get('/teams', response_model=List[Team])
def read_teams(coach_id: int = Query(..., description="The ID of the coach")):
    # fetch the list of teams related to the coach
    teams = get_teams_by_coach_id(session, coach_id)
    return teams


# Endpoint to add a new team
class TeamCreateRequest(BaseModel):
    coach_id: int
    team_name: str
    primary_color: str
    secondary_color: str

@app.post('/teams', response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team_req(team_request: TeamCreateRequest):
    # Check if the coach exists
    coach = get_coach_by_id(session, team_request.coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    else:
        team = create_team(session, team_request.coach_id, team_request.team_name, team_request.primary_color, team_request.secondary_color)
        return team


# Endpoint to get the list of players
class Player(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str | None
    birthDate: str
    number: int | None
    position: str | None
    deviceId: str | None # A player might not have a device
    lineNum: int | None # A player might not be assigned to a line
    isOffense: bool | None # A player might not be assigned to a line
    deviceStatus: str | None # A player might not have a device
    maxHR: int | None
    restHR: int | None

def transform_players(players):
    transformed_players = []
    # Get the timestamp 60 seconds ago, to determine if a device is connected or not
    ts_60_sec_ago = datetime.now() - timedelta(seconds=60)
    for player, line, device_id, latest_timestamp, max_HR, rest_HR in players:
        transformed_player = {
            "id": player.id,
            "firstName": player.first_name,
            "lastName": player.last_name,
            "email": player.email if player.email else None,
            "birthDate": player.birth_date.strftime("%Y-%m-%d"),
            "number": player.number,
            "position": player.position,
            "lineNum": line.line_number if line else None,
            "isOffense": line.is_offense if line else None,
            "deviceId": device_id if device_id else None,
            "deviceStatus": "Connected" if latest_timestamp and latest_timestamp > ts_60_sec_ago else "Disconnected",
            "maxHR": max_HR if max_HR else None,
            "restHR": rest_HR if rest_HR else None
        }
        transformed_players.append(transformed_player)
    return transformed_players

@app.get('/players', response_model=List[Player])
async def read_players(team_id: int = Query(..., description="The ID of the team")):
    players = get_players_by_team(session, team_id)
    return transform_players(players)

# Schéma Pydantic pour créer un joueur
class PlayerCreateRequest(BaseModel):
    team_id: int
    first_name: str
    last_name: str
    birth_date: str
    email: str

class PlayerCreated(BaseModel):
    id: int
    team_id: int
    line_id: Optional[int]
    first_name: str
    last_name: str
    birth_date: str
    position: Optional[str]
    email: Optional[str]
    number: Optional[int]

@app.post('/players', status_code=status.HTTP_201_CREATED, response_model=PlayerCreated)
async def create_players_req(player_create: PlayerCreateRequest):
    player = create_player(session, player_create.team_id, player_create.first_name, player_create.last_name, player_create.birth_date, player_create.email)
    player_created = PlayerCreated(id=player.id, team_id=player.team_id, line_id=player.line_id, first_name=player.first_name, last_name=player.last_name, birth_date=player.birth_date.strftime("%Y-%m-%d"), position=player.position, email=player.email, number=player.number)
    return player_created

# Schéma Pydantic pour éditer un joueur
class PlayerUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    email: str
    number: int | None
    position: str | None

@app.put('/players/{player_id}', status_code=status.HTTP_200_OK)
async def update_player_req(player_id: int, player_update: PlayerUpdateRequest):
    # Fetch the player from the database
    player = update_player(session, player_id, player_update.first_name, player_update.last_name, datetime.strptime(player_update.birth_date, "%Y-%m-%d"), player_update.email, player_update.number, player_update.position)

    # Verify if player exists
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Player updated successfully"}

class PlayerHealthUpdateRequest(BaseModel):
    max_HR: int
    rest_HR: int

@app.post('/players/{player_id}/health', status_code=status.HTTP_200_OK)
async def update_player_health(player_id: int, health_update: PlayerHealthUpdateRequest):
    game_medical_data = add_game_medical_data(session, player_id, health_update.rest_HR, health_update.max_HR)
    if game_medical_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Player health updated successfully"}


@app.post('/players/{player_id}/health/default', status_code=status.HTTP_200_OK, response_model=PlayerHealthUpdateRequest)
async def set_default_player_health(player_id: int):
    # Fetch the player from the database
    game_medical_data = add_default_game_medical_data(session, player_id)

    # Verify if player exists
    if game_medical_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "max_HR": game_medical_data.max_HR,
        "rest_HR": game_medical_data.rest_HR
    }


# Endpoint to associate a player to a device
class PlayerDeviceUpdateRequest(BaseModel):
    player_id: int
    device_id: str

@app.post('/devices', status_code=status.HTTP_200_OK)
async def update_player_device(device_update: PlayerDeviceUpdateRequest):
    player_device_at = add_player_device_at(session, device_update.player_id, device_update.device_id)

    # Verify if player and device exist
    if player_device_at is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player or device not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Player device updated successfully"}


# Endpoint to connect to a device (and start data generation)
@app.post('/{team_id}/devices/{device_id}/connect', status_code=status.HTTP_200_OK)
async def connect_device(team_id: int, device_id: str):
    # Start the data generator in the background
    global background_tasks
    print("Starting data generator for device " + device_id)
    if device_id not in background_tasks:
        background_tasks[device_id] = asyncio.create_task(generate_hr_data(device_id, team_id))
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Task started for device " + device_id})
    else:
        print(f"Task for device {device_id} is already running")
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"message": f"Task for device {device_id} is already running"})


# Endpoint to connect all players to their device (and start data generation)
@app.post('/{team_id}/devices/connect', status_code=status.HTTP_200_OK)
async def connect_all_devices(team_id: int):
    # Get the list of players with a device that are a part of the team
    players_and_devices = get_players_devices_on_team(session, team_id)
    global background_tasks
    response = JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Task started for all devices"})
    for player, device_id in players_and_devices:
        print(f"Starting task for player {player} and device {device_id}")
        if device_id is None:
            print(f"No device found for player {player}")
        elif device_id not in background_tasks:
            background_tasks[device_id] = asyncio.create_task(generate_hr_data(device_id, team_id))
        else:
            print(f"Task for device {device_id} is already running")
            response = JSONResponse(status_code=status.HTTP_409_CONFLICT,
                                content={"message": f"Task for device {device_id} is already running"})
    return response

# Endpoint to disconnect all players from their device (and stop data generation)
@app.post('/{team_id}/devices/disconnect', status_code=status.HTTP_200_OK)
async def disconnect_all_devices(team_id: int):
    global background_tasks
    device_ids = list(background_tasks.keys())  # Create a list of keys to iterate over
    for device_id in device_ids:
        print(f"Stopping data generator for device {device_id}")
        background_tasks[device_id].cancel()
        try:
            await background_tasks[device_id]
        except asyncio.CancelledError:
            print("Task cancelled successfully.")
        del background_tasks[device_id]


# Endpoint to disconnect from a device
@app.post('/{team_id}/devices/{device_id}/disconnect', status_code=status.HTTP_200_OK)
async def disconnect_device(team_id: int, device_id: str):
    print("Stopping data generator for device " + device_id)
    global background_tasks
    if device_id in background_tasks:
        background_tasks[device_id].cancel()
        try:
            await background_tasks[device_id]
        except asyncio.CancelledError:
            print("Task cancelled successfully.")
        del background_tasks[device_id]
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Task stopped for device " + device_id})
    else:
        print(f"No task found for device {device_id}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"message": f"No task found for device {device_id}"})


# Endpoint to get the lines
class PlayerLine(BaseModel):
    playerId: int
    firstName: str
    lastName: str
    number: int
    lineId: Optional[int]
    position: str

class Line(BaseModel):
    lineId: int
    lineNum: int
    isOffense: bool

@app.get('/lines', response_model=List[Line])
def read_lines(team_id: int = Query(..., description="The ID of the team")):
    lines = get_lines(session, team_id)
    transformed_lines = []
    for line in lines:
        transformed_line = {
            "lineId": line.id,
            "lineNum": line.line_number,
            "isOffense": line.is_offense
        }
        transformed_lines.append(transformed_line)
    print(transformed_lines)
    return transformed_lines



@app.get('/lines/players', response_model=List[PlayerLine])
def read_players_line(team_id: int = Query(..., description="The ID of the team")):
    player_lines = get_players_line(session, team_id)
    transformed_player_lines = []
    for player_line in player_lines:
        transformed_player_line = {
            "playerId": player_line.id,
            "firstName": player_line.first_name,
            "lastName": player_line.last_name,
            "number": player_line.number,
            "lineId": player_line.line_id,
            "position": player_line.position
        }
        transformed_player_lines.append(transformed_player_line)
    print(transformed_player_lines)
    return transformed_player_lines

@app.delete('/lines/players/{playerId}', status_code=status.HTTP_200_OK)
def remove_player_line(playerId: int):
    # Remove the player from the line
    removed_player = remove_player_from_line(session, playerId)
    if removed_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Player removed from line successfully"}

@app.post('/lines/{lineId}/players/{playerId}', status_code=status.HTTP_201_CREATED)
def add_player_line(lineId: int, playerId: int):
    # verify if the line exists
    line = get_line_by_id(session, lineId)
    if line is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Line not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        # Add the player to the line
        player = add_player_to_line(session, playerId, lineId)
        if player is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"message": "Player added to line successfully"}


# Endpoint to get the players states
class PlayerStats(BaseModel):
    playerId: int
    firstName: str
    lastName: str
    number: int
    lineNum: int
    isOffense: bool
    hr: int
    state: str
    recScore: int
    gameId: int

def get_players_stats(team_id: int) -> List[PlayerStats]:
    # Get the current game
    game = get_team_current_game(session, team_id)

    # Get the players with a line
    players = get_player_on_line_by_team_id(session, team_id)
    player_stats = []
    # For each player, get the player state
    for player in players:
        player_state = get_player_state_by_player_and_game_id(session, player.Player.id, game.id)
        player_stat = PlayerStats(
            playerId=player.Player.id,
            lineNum=player.line_number,
            isOffense=player.is_offense,
            hr=player_state.heart_rate,
            state=player_state.state,
            recScore=player_state.rec_score,
            gameId=player_state.game_id,
            firstName=player.Player.first_name,
            lastName=player.Player.last_name,
            number=player.Player.number
        )
        player_stats.append(player_stat)

    return player_stats


@app.get('/players-stats', response_model=List[PlayerStats])
def read_line_status(team_id: int = Query(..., description="The ID of the team")):
    players_stats = get_players_stats(team_id)
    print(players_stats)
    return players_stats


# Websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Listen for messages from the client
            data = await websocket.receive_text()
            await websocket_manager.send_message(f"Message received: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)