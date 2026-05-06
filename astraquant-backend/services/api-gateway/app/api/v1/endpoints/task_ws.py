from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["websocket"])

@router.websocket("/api/ws/tasks")
async def task_websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"event_type": "connected", "message": "task websocket connected"})
    await websocket.close()
