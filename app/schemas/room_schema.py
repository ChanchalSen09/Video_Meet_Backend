from pydantic import BaseModel

class RoomCreateResponse(BaseModel):
    room_id: str
    host_email: str
