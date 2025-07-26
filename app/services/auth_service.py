from fastapi import HTTPException, status
from app.db.mongo import db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user_model import user_response

async def register_user(name: str, email: str, password: str):
    user = await db.users.find_one({"email": email})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = hash_password(password)
    new_user = {"name": name, "email": email, "password": hashed_pwd}
    result = await db.users.insert_one(new_user)
    saved_user = await db.users.find_one({"_id": result.inserted_id})
    return user_response(saved_user)

async def login_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer", "user": user_response(user)}
