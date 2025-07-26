from fastapi import APIRouter, Depends
from app.services.room_service import create_room, join_room
from app.utils.deps import get_current_user

router = APIRouter()

@router.post("/create-room")
async def create_new_room(current_user: str = Depends(get_current_user)):
    return await create_room(current_user)

@router.get("/join-room/{room_id}")
async def join_existing_room(room_id: str):
    return await join_room(room_id)
