from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.core.security import decode_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    FastAPI dependency to get the current authenticated user from the JWT token.
    
    Args:
        credentials: Automatically injected HTTPAuthorizationCredentials by FastAPI.
        
    Returns:
        The 'sub' claim from the JWT payload, commonly the user's unique identifier (e.g., email).
    
    Raises:
        HTTPException: If the token is invalid or missing, returns 401 Unauthorized.
    """
    token = credentials.credentials
    try:
        payload = decode_token(token)
        user_sub = payload.get("sub")
        if user_sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload missing 'sub' claim",
            )
        return user_sub
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
