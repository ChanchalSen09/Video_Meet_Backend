from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter()

rooms: Dict[str, List[WebSocket]] = {}

@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()

    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(websocket)

    for conn in rooms[room_id]:
        if conn != websocket:
            await conn.send_json({"type": "user-joined", "user": user_id})

    try:
        while True:
            data = await websocket.receive_json()
            for conn in rooms[room_id]:
                if conn != websocket:
                    await conn.send_json({
                        "from": user_id,
                        "data": data
                    })
    except WebSocketDisconnect:
        rooms[room_id].remove(websocket)
        if not rooms[room_id]:
            del rooms[room_id]
        for conn in rooms.get(room_id, []):
            await conn.send_json({"type": "user-left", "user": user_id})
