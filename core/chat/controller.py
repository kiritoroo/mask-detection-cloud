from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import datetime
import json

templates = Jinja2Templates(directory="templates")
websocket_router = APIRouter()

class ConnectionManager:

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@websocket_router.route(path='/chat', methods=['GET', 'POST'])
def main(request: Request):
    auth = request.cookies.get("jwt")
    if auth == None:
        return templates.TemplateResponse(
            "pages/login.html",
            {
                "request": request,
                "user": {"username": ""},
                "message": "Enter username and password"
            }
        )
    
    return templates.TemplateResponse(
        "pages/chat.html",
        {
            "request": request,
        }
    )

@websocket_router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    try:
        while True:
            data = await websocket.receive_text()
            message = {"time":current_time, "clientId":username, "message":data}
            await manager.broadcast(json.dumps(message))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time":current_time, "clientId":username, "message": "Offline"}
        await manager.broadcast(json.dumps(message))

