from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RoomCreateResponse(BaseModel):
    room_id: str
    host_email: EmailStr  # Use EmailStr for validation here

class RoomResponse(RoomCreateResponse):
    created_at: datetime

    class Config:
        orm_mode = True
