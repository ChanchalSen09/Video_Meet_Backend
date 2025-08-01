from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponseModel(BaseModel):
    id: str
    name: str
    email: EmailStr
    picture: str = ""  # Optional profile image

    model_config = ConfigDict(from_attributes=True)
