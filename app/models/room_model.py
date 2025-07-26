def room_response(room: dict) -> dict:
    return {
        "room_id": room["room_id"],
        "host_email": room["host_email"],
        "created_at": room["created_at"]
    }
