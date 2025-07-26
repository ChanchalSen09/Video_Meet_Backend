from datetime import datetime
import uuid
from app.db.mongo import db
from app.models.room_model import room_response
from fastapi import HTTPException

async def create_room(host_email: str):
    room_id = str(uuid.uuid4())[:8]  # short unique id
    room = {
        "room_id": room_id,
        "host_email": host_email,
        "created_at": datetime.utcnow()
    }
    await db.rooms.insert_one(room)
    return room_response(room)

async def join_room(room_id: str):
    room = await db.rooms.find_one({"room_id": room_id})
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room_response(room)
