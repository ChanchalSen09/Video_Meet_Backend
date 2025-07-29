from fastapi import APIRouter, Depends, HTTPException
from app.services.room_service import create_room, request_join_room, approve_user
from app.utils.deps import get_current_user

router = APIRouter(tags=["Rooms"])

@router.post("/create-room")
async def create_new_room(current_user: str = Depends(get_current_user)):
    return await create_room(current_user)

@router.get("/request-join/{room_id}")
async def request_join(room_id: str, current_user: str = Depends(get_current_user)):
    return await request_join_room(room_id, current_user)

@router.post("/approve-user")
async def approve_participant(room_id: str, user_email: str, current_user: str = Depends(get_current_user)):
    return await approve_user(room_id, current_user, user_email)
