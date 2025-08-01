from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests
from app.db.mongo import db
from app.schemas.user_schema import UserResponseModel
from app.core.security import create_access_token

# Your actual Google Client ID here
GOOGLE_CLIENT_ID = "407408718192.apps.googleusercontent.com"

async def google_authenticate(token: str):
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # Extract user info
        email = idinfo.get("email")
        name = idinfo.get("name", "No Name")
        picture = idinfo.get("picture", "")

        if not email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found in token")

        # Check if user exists in MongoDB
        user = await db.users.find_one({"email": email})
        if not user:
            # Create new user
            new_user = {"name": name, "email": email, "picture": picture}
            result = await db.users.insert_one(new_user)
            user = await db.users.find_one({"_id": result.inserted_id})

        # Generate access token
        jwt = create_access_token({"sub": email})

        # Respond
        return {
            "access_token": jwt,
            "token_type": "bearer",
            "user": UserResponseModel(
                id=str(user["_id"]),
                name=user.get("name", ""),
                email=user.get("email", ""),
                picture=user.get("picture", ""),
            )
        }

    except ValueError as e:
        print("Google token verification failed:", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token")
