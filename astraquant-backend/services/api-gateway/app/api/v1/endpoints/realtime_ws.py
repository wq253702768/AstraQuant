from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["websocket"])

@router.websocket("/api/ws/realtime")
async def realtime_websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"event_type": "connected", "message": "realtime websocket connected"})
    await websocket.close()
