from fastapi import WebSocket, APIRouter, WebSocketDisconnect

router = APIRouter()    

connected_clients: set[WebSocket] = set()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"Client connected: {websocket.client}")
    try:
        while True:
            data = await websocket.receive_text()
            for client in connected_clients:
                await client.send_text(f"Client {websocket.client} said: {data}")
    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")
        connected_clients.remove(websocket)