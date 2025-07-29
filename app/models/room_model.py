from typing import TypedDict

class RoomDict(TypedDict):
    room_id: str
    host_email: str
    created_at: str 

def room_response(room: RoomDict) -> dict:
    return {
        "room_id": room["room_id"],
        "host_email": room["host_email"],
        "created_at": room["created_at"]
    }
