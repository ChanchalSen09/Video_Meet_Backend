from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class RoomCreateResponse(BaseModel):
    room_id: str
    host_email: EmailStr  # Email validation

class RoomResponse(RoomCreateResponse):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
