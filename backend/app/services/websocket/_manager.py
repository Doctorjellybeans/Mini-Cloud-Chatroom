from typing import Set, Any, Dict
import logging
import asyncio
from datetime import datetime
from fastapi import WebSocket

class WebSocketManager:
    """
    Manager que rastrea websockets, usuarios y rooms.

    Mantiene:
    - active_connections: set de todos los websockets actualmente conectados
    - ws_to_user: Dict[WebSocket, str]: mapea websocket a username
    - user_to_ws: Dict[str, WebSocket]: mapea username a websocket
    - rooms: Dict[str, Set[WebSocket]]: mapea nombre de room a set de websockets conectados

    Metodos:
    - connect(websocket): acepta nueva conexion y la agrega a active_connections
    - disconnect(websocket): elimina conexion de active_connections y de cualquier room, y limpia mapeos de usuario si es necesario
    - is_username_taken(username): verifica si el username ya esta registrado
    - register_user(websocket, username): registra el websocket con el username dado
    - get_username(websocket): obtiene el username registrado para un websocket, o None si no esta registrado
    - join_room(websocket, room): agrega el websocket a la room dada
    - leave_room(websocket, room): elimina el websocket de la room dada
    - broadcast_room(room, data): dependiendo del tipo de evento emite un mensaje a todos los websockets. Tipos de evento:
        - user_joined: notifica a la room que un usuario se ha unido
        - user_left: notifica a la room que un usuario ha salido
        - user_disconnected: notifica a la room que un usuario se ha desconectado

     - broadcast_system_message(room, text): helper para enviar un mensaje de sistema a una room con formato estandarizado
    """
    
    def __init__(self) -> None:
        self.active_connections: Set[WebSocket] = set()
        self.ws_to_user: Dict[WebSocket, str] = {}
        self.ws_to_room: Dict[WebSocket, str] = {}
        self.user_to_ws: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, Set[WebSocket]] = {}
        self.logger = logging.getLogger("websocket.manager") # Crea un logger en caso de que no encuentre ningun logger
        self.clientName = None

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        self.logger.debug("Accepted connection: %s", getattr(websocket, "client", None))
        self.clientName = getattr(websocket, "client", None)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)

        username = self.ws_to_user.pop(websocket, None)
        if username:
            self.user_to_ws.pop(username, None)

        room = self.ws_to_room.pop(websocket, None)
        if room:
            # Si el websocket estaba en una sala, eliminarlo y notificar a los demas usuarios en la sala
            conns = self.rooms.get(room)
            if conns and websocket in conns:
                conns.discard(websocket)
                if not conns:
                    self.rooms.pop(room, None)
            try:
                # Emit specific disconnect event
                await self.broadcast_event(room, 'user_disconnected', username or 'unknown', f"{username or 'unknown'} has disconnected")
            except Exception:
                # Error durante el broadcast de desconexion
                self.logger.exception('Error broadcasting disconnect for %s', getattr(websocket, 'client', None))

        self.logger.debug("Disconnected: %s", getattr(websocket, "client", None))

    def is_username_taken(self, username: str) -> bool:
        return username in self.user_to_ws


    async def register_user(self, websocket: WebSocket, username: str) -> None:
        
        self.ws_to_user[websocket] = username
        self.user_to_ws[username] = websocket
        self.clientName = username
        self.logger.debug("Registered user %s for %s", username, getattr(websocket, "client", None))
    
    def get_username(self, websocket: WebSocket) -> str | None:
        return self.ws_to_user.get(websocket)

    async def join_room(self, websocket: WebSocket, room: str) -> None:
        prev = self.ws_to_room.get(websocket)
        username = self.get_username(websocket) or 'unknown'

        if prev and prev != room:
            prev_conns = self.rooms.get(prev)
            if prev_conns and websocket in prev_conns:
                prev_conns.discard(websocket)
                if not prev_conns:
                    self.rooms.pop(prev, None)
            await self.broadcast_event(prev, 'user_left', username, f"{username} has left the room")

        conns = self.rooms.setdefault(room, set())
        conns.add(websocket)
        self.ws_to_room[websocket] = room
        self.logger.debug("Websocket %s joined room %s", getattr(websocket, "client", None), room)

        await self.broadcast_event(room, 'user_joined', username, f"{username} has joined the room")

    async def leave_room(self, websocket: WebSocket, room: str) -> None:
        username = self.get_username(websocket) or 'unknown'
        conns = self.rooms.get(room)
        if conns and websocket in conns:
            conns.discard(websocket)
            if not conns:
                self.rooms.pop(room, None)

        if self.ws_to_room.get(websocket) == room:
            self.ws_to_room.pop(websocket, None)

        await self.broadcast_event(room, 'user_left', username, f"{username} has left the room")

    async def broadcast_event(self, room: str, event_type: str, username: str, text: str | None = None) -> None:
        try:
            ts = datetime.utcnow().isoformat() + 'Z'
            payload = {
                'type': event_type,
                'room': room,
                'user': username or 'unknown',
                'text': text or '',
                'ts': ts,
            }
            await self.broadcast_room(room, payload)
        except Exception:
            self.logger.exception('Error broadcasting event %s for room %s', event_type, room)
    
    async def broadcast_room(self, room: str, data: Any) -> None:
        conns = self.rooms.get(room)
        if not conns:
            return
        to_remove = []
        for conn in list(conns):
            try:
                await conn.send_json(data)
            except Exception as exc:
                self.logger.debug("Removing dead connection %s after error: %s", getattr(conn, "client", None), exc)
                to_remove.append(conn)
        for conn in to_remove:
            await self.disconnect(conn)