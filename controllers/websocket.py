from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.chat_service import ChatService


router = APIRouter(
    prefix="/ws",
    tags=["Websocket"]
)

chatService = ChatService()


@router.websocket("/{username}")
async def websocket(websocket: WebSocket, username: str):
    await chatService.on_open(websocket=websocket, username=username)
    try:
        while True:
            data = await websocket.receive_text()
            await chatService.on_message(username=username, message=data)
    except WebSocketDisconnect:
        await chatService.on_close(username=username)
