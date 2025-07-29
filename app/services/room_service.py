from datetime import datetime
import uuid
from fastapi import HTTPException
from app.db.mongo import db
from app.models.room_model import room_response

async def create_room(host_email: str):
    room_id = str(uuid.uuid4())[:8]  
    room = {
        "room_id": room_id,
        "host_email": host_email,
        "created_at": datetime.utcnow(),
        "participants": [],
        "pending_requests": []  # NEW FIELD
    }
    await db.rooms.insert_one(room)
    return room_response(room)

async def request_join_room(room_id: str, user_email: str):
    room = await db.rooms.find_one({"room_id": room_id})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Prevent duplicate requests
    if user_email in room.get("participants", []) or user_email in room.get("pending_requests", []):
        return {"status": "already_joined_or_pending"}

    await db.rooms.update_one(
        {"room_id": room_id},
        {"$addToSet": {"pending_requests": user_email}}
    )
    return {"status": "request_sent"}

async def approve_user(room_id: str, host_email: str, user_email: str):
    room = await db.rooms.find_one({"room_id": room_id})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if room["host_email"] != host_email:
        raise HTTPException(status_code=403, detail="Only host can approve")

    await db.rooms.update_one(
        {"room_id": room_id},
        {
            "$pull": {"pending_requests": user_email},
            "$addToSet": {"participants": user_email}
        }
    )
    return {"message": f"{user_email} has been approved to join"}
