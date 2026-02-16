from fastapi import WebSocket, APIRouter, WebSocketDisconnect
import logging
import json
from datetime import datetime, timezone

from backend.app.services.websocket._manager import WebSocketManager

router = APIRouter()

logger = logging.getLogger("backend.websocket")

# App principal que maneja las conexiones, desconexiones y mensajes del o los websockets
manager = WebSocketManager()

# Formatear hora min y seg
def _now_iso() -> str:
    return "".join(i for i in datetime.now(timezone.utc).isoformat())



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info("Client connected: %s", getattr(websocket, "client", None))

    try:
        # Esperamos el msg de el join
        raw = await websocket.receive_text()
        try:
            msg = json.loads(raw)
        except Exception:
            await websocket.send_json({"type": "join_response", "ok": False, "reason": "invalid_json"})
            await manager.disconnect(websocket)
            return

        if msg.get("type") != "join" or not msg.get("user"):
            await websocket.send_json({"type": "join_response", "ok": False, "reason": "missing_join"})
            await manager.disconnect(websocket)
            return

        username = msg["user"].strip()
        initial_room = msg.get("room")

        if manager.is_username_taken(username):
            await websocket.send_json({"type": "join_response", "ok": False, "reason": "username_taken"})
            await manager.disconnect(websocket)
            return

        # Registro de usuarios y unión a sala inicial 
        await manager.register_user(websocket, username)
        if initial_room:
            await manager.join_room(websocket, initial_room)

        await websocket.send_json({"type": "join_response", "ok": True})

        # Loop principal para el manejo de mensajes
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                await websocket.send_json({"type": "error", "msg": "invalid_json"})
                continue

            mtype = msg.get("type")
            if mtype == "join_room":
                room = msg.get("room")
                if room:
                    await manager.join_room(websocket, room)
                    await websocket.send_json({"type": "join_room_response", "ok": True, "room": room})
                else:
                    await websocket.send_json({"type": "join_room_response", "ok": False, "reason": "no_room"})

            elif mtype == "leave_room":
                room = msg.get("room")
                if room:
                    await manager.leave_room(websocket, room)
                    await websocket.send_json({"type": "leave_room_response", "ok": True, "room": room})
                else:
                    await websocket.send_json({"type": "leave_room_response", "ok": False, "reason": "no_room"})

            elif mtype == "message":
                room = msg.get("room")
                text = msg.get("text")
                if not room or not text:
                    await websocket.send_json({"type": "error", "msg": "missing_room_or_text"})
                    continue
                user = manager.get_username(websocket) or "unknown"
                out = {
                    "type": "message",
                    "room": room,
                    "user": user,
                    "text": text,
                    "ts": _now_iso(),
                }
                await manager.broadcast_room(room, out)

            else:
                await websocket.send_json({"type": "error", "msg": "unknown_type"})

    except WebSocketDisconnect:
        logger.info("Client disconnected: %s", getattr(websocket, "client", None))
        await manager.disconnect(websocket)
    except Exception as exc:  # ensure we clean up on unexpected errors
        logger.exception("WebSocket error for %s: %s", getattr(websocket, "client", None), exc)
        await manager.disconnect(websocket)