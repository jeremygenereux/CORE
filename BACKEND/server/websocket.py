from fastapi import WebSocket
from typing import List
import json

class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Connected to websocket")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Disconnected from websocket")

    async def send_message(self, message: dict):
        print("Sending message to websocket")
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))
            print("Sent message to websocket")

    async def send_str_message(self, message: str):
        print("Sending message to websocket")
        for connection in self.active_connections:
            await connection.send_text(message)
            print("Sent message to websocket")