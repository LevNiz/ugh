from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from typing import Dict, List
from app import schemas, crud, deps

router = APIRouter()

@router.post("/create_chat")
async def create_chat(
    chat_data: schemas.ChatCreate,
    db=Depends(deps.get_db)
):

    new_chat = await crud.create_chat(db, chat_data)
    print("new chat:", new_chat)
    return new_chat

@router.get("/my_chats", response_model=List[schemas.Chat])
async def get_my_chats(current_user: schemas.User = Depends(deps.get_current_user), db=Depends(deps.get_db)):
    chats = await crud.get_chats_by_user(db, current_user['id'])
    return chats

@router.get("/chat_messages/{chat_id}")
async def get_chat_messages(chat_id: int, current_user: schemas.User = Depends(deps.get_current_user), db=Depends(deps.get_db)):
    messages = await crud.get_messages_by_chat(db, chat_id)
    return messages

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        self.active_connections.append((websocket, chat_id))

    def disconnect(self, websocket: WebSocket, chat_id: int):
        self.active_connections = [(ws, cid) for ws, cid in self.active_connections if ws != websocket and cid != chat_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, chat_id: int, message: dict):
        for connection, cid in self.active_connections:
            if cid == chat_id:
                await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, token: str = Query(...), db=Depends(deps.get_db)):
    try:
        current_user = await deps.get_current_user(token, db)
    except HTTPException as e:
        await websocket.close(code=1008)
        print(f"Connection rejected: {e.detail}")
        return
    
    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = schemas.MessageCreate(chat_id=chat_id, sender_id=current_user['id'], content=data)
            new_message = await crud.create_message(db, message_data)
            await manager.broadcast_message(chat_id, record_to_dict(new_message))
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)



def record_to_dict(record):
    result = dict(record)
    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
    return result