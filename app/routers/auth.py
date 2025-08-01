from fastapi import APIRouter, Body
from app.services.auth_service import google_authenticate
from app.schemas.user_schema import UserResponseModel

router = APIRouter(tags=["Authentication"])

@router.post("/google")
async def google_login(id_token: str = Body(..., embed=True)):
    return await google_authenticate(id_token)
