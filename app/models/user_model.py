from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, ConfigDict
from typing import Any

def objectid_str(oid: Any) -> str:
    return str(oid) if oid else ""

class UserResponseModel(BaseModel):
    id: str
    name: str
    email: EmailStr 

    model_config = ConfigDict(from_attributes=True)

def user_response(user: dict) -> UserResponseModel:
    return UserResponseModel(
        id=str(user.get("_id")),
        name=user.get("name", ""),
        email=user.get("email", "")
    )
