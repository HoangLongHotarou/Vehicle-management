from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.activate_connection: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activate_connection.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.activate_connection.remove(websocket)
    
    def check_contain(self,websocket: WebSocket):
        return websocket in self.activate_connection
    
    async def send_personal_message(self,message: str,websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self,message):
        for connection in self.activate_connection:
            await connection.send_json(message)



class ConnectionManagerV2:
    def __init__(self):
        self.activate_connection={}
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activate_connection[websocket] = ''
    
    def disconnect(self, websocket: WebSocket):
        self.activate_connection.pop(websocket)
    
    def set_state_connection(self,websocket: WebSocket,status: str):
        value = self.activate_connection.get(websocket)
        if value == None: return
        self.activate_connection[websocket]=status
    
    async def send_personal_message(self,websocket: WebSocket,message: str):
        await websocket.send_text(message)
    
    async def broadcast(self,message,status):
        for websocket in self.activate_connection:
            if self.activate_connection[websocket]==str(status):
                await websocket.send_json(message)