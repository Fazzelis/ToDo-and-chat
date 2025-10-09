from fastapi import WebSocket, WebSocketException


class ChatService:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def on_open(self, websocket: WebSocket, username: str):
        if not(3 < len(username) < 20):
            raise WebSocketException(code=1007, reason="Слишком длинное имя")
        if username in self.active_connections:
            raise WebSocketException(code=1007, reason="Такое имя уже занято")
        await websocket.accept()
        self.active_connections[username] = websocket
        for ws in self.active_connections.values():
            message = f"{username} присоединился к чату"
            await ws.send_text(message)

    async def on_close(self, username: str):
        del self.active_connections[username]
        for ws in self.active_connections.values():
            message = f"{username} покинул чат"
            await ws.send_text(message)

    async def on_message(self, username: str, message: str):
        if username in self.active_connections:
            for un, websocket in self.active_connections.items():
                response = {
                    "username": username,
                    "message": message
                }
                await websocket.send_json(response)
