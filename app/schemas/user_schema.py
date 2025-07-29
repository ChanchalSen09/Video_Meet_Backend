from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
