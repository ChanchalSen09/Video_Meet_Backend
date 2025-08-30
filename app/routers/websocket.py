# app/routers/websocket.py  (full updated)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Any

router = APIRouter()

rooms: Dict[str, Dict[str, Any]] = {}

async def safe_send(ws: WebSocket, payload: dict):
    try:
        await ws.send_json(payload)
    except Exception:
        pass

def ensure_room(room_id: str):
    if room_id not in rooms:
        rooms[room_id] = {"host": None, "guests": {}, "pending": {}, "status": {}}  # status: {user_id: {muted:bool, cam:bool}}

@router.websocket("/ws/{room_id}/{user_id}/{role}")
async def ws_endpoint(websocket: WebSocket, room_id: str, user_id: str, role: str):
    await websocket.accept()
    ensure_room(room_id)

    room = rooms[room_id]
    # default status
    room["status"][user_id] = {"muted": False, "camera": True}

    if role == "host":
        room["host"] = {"id": user_id, "ws": websocket}
        if room["pending"]:
            await safe_send(websocket, {"type": "pending-list", "users": list(room["pending"].keys())})
        if room["guests"]:
            await safe_send(websocket, {"type": "participants", "users": list(room["guests"].keys())})
        # send current status map
        await safe_send(websocket, {"type": "status-map", "status": room["status"]})
    else:
        room["pending"][user_id] = websocket
        if room["host"]:
            await safe_send(room["host"]["ws"], {"type": "join-request", "user": user_id})

    try:
        while True:
            msg = await websocket.receive_json()
            mtype = msg.get("type")

            # Host actions
            if role == "host":
                if mtype == "approve":
                    guest_id = msg["user"]
                    guest_ws = room["pending"].pop(guest_id, None)
                    if guest_ws:
                        room["guests"][guest_id] = guest_ws
                        room["status"].setdefault(guest_id, {"muted": False, "camera": True})
                        await safe_send(guest_ws, {"type": "approved"})
                        await safe_send(websocket, {"type": "participant-joined", "user": guest_id})
                        # broadcast new participant to all guests (optional)
                        for gid, gws in room["guests"].items():
                            if gid != guest_id:
                                await safe_send(gws, {"type": "new-participant", "user": guest_id})

                elif mtype == "reject":
                    guest_id = msg["user"]
                    guest_ws = room["pending"].pop(guest_id, None)
                    if guest_ws:
                        await safe_send(guest_ws, {"type": "rejected"})

                elif mtype in ("offer", "answer", "ice"):
                    to_user = msg.get("to")
                    payload = {k: v for k, v in msg.items() if k != "to"}
                    if to_user and to_user in room["guests"]:
                        await safe_send(room["guests"][to_user], payload)
                    else:
                        for gid, gws in room["guests"].items():
                            await safe_send(gws, payload)

                elif mtype == "control":  # host broadcasting a control (mute/camera) update (host can toggle others)
                    target = msg.get("user")
                    action = msg.get("action")  # "mute" | "unmute" | "camera-off" | "camera-on"
                    if target:
                        status = room["status"].setdefault(target, {"muted": False, "camera": True})
                        if action == "mute":
                            status["muted"] = True
                        elif action == "unmute":
                            status["muted"] = False
                        elif action == "camera-off":
                            status["camera"] = False
                        elif action == "camera-on":
                            status["camera"] = True
                        # notify target and host
                        target_ws = room["guests"].get(target)
                        if target_ws:
                            await safe_send(target_ws, {"type": "control", "action": action})
                        await safe_send(websocket, {"type": "status-update", "user": target, "status": status})

            # Guest actions (signaling, or guest control for themselves)
            else:
                if mtype in ("offer", "answer", "ice"):
                    if room["host"]:
                        payload = {"from": user_id, **msg}
                        await safe_send(room["host"]["ws"], payload)

                elif mtype == "control":
                    # guest toggles their own mute/camera; update status and broadcast to host + other guests
                    action = msg.get("action")
                    status = room["status"].setdefault(user_id, {"muted": False, "camera": True})
                    if action == "mute":
                        status["muted"] = True
                    elif action == "unmute":
                        status["muted"] = False
                    elif action == "camera-off":
                        status["camera"] = False
                    elif action == "camera-on":
                        status["camera"] = True

                    # notify host
                    if room["host"]:
                        await safe_send(room["host"]["ws"], {"type": "status-update", "user": user_id, "status": status})
                    # notify other guests
                    for gid, gws in room["guests"].items():
                        if gid != user_id:
                            await safe_send(gws, {"type": "status-update", "user": user_id, "status": status})

    except WebSocketDisconnect:
        if role == "host":
            room["host"] = None
            for gid, gws in list(room["guests"].items()):
                await safe_send(gws, {"type": "host-left"})
        else:
            if user_id in room["guests"]:
                room["guests"].pop(user_id, None)
                room["status"].pop(user_id, None)
                if room["host"]:
                    await safe_send(room["host"]["ws"], {"type": "participant-left", "user": user_id})
                # notify remaining guests
                for gid, gws in room["guests"].items():
                    await safe_send(gws, {"type": "participant-left", "user": user_id})
            else:
                room["pending"].pop(user_id, None)
                room["status"].pop(user_id, None)

        if not room["host"] and not room["guests"] and not room["pending"]:
            rooms.pop(room_id, None)
