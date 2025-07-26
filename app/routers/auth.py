from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    return await register_user(user.name, user.email, user.password)

@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user.email, user.password)
