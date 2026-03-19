from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.db.database import get_database
from jose import JWTError


async def register_user(username: str, email: str, password: str) -> dict:
    db = await get_database()

    # Check uniqueness
    if await db["users"].find_one({"email": email}):
        raise HTTPException(status_code=409, detail="Email already registered")
    if await db["users"].find_one({"username": username}):
        raise HTTPException(status_code=409, detail="Username already taken")

    # First user becomes admin automatically
    is_first_user = await db["users"].count_documents({}) == 0
    role = "admin" if is_first_user else "user"

    user_doc = {
        "username": username,
        "email": email,
        "hashed_password": hash_password(password),
        "role": role,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await db["users"].insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc


async def authenticate_user(email: str, password: str) -> dict:
    db = await get_database()
    user = await db["users"].find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Account is deactivated")
    return user


def _issue_tokens(user: dict) -> dict:
    payload = {"sub": str(user["_id"]), "role": user["role"]}
    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
    }


async def login_user(email: str, password: str) -> dict:
    user = await authenticate_user(email, password)
    return _issue_tokens(user)


async def refresh_access_token(refresh_token: str) -> dict:
    db = await get_database()

    # Check blacklist
    if await db["token_blacklist"].find_one({"token": refresh_token}):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return _issue_tokens(user)


async def logout_user(refresh_token: str):
    """Blacklist the refresh token."""
    db = await get_database()
    try:
        payload = decode_token(refresh_token)
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    await db["token_blacklist"].update_one(
        {"token": refresh_token},
        {"$set": {"token": refresh_token, "expires_at": expires_at}},
        upsert=True,
    )


async def get_user_by_id(user_id: str) -> dict:
    db = await get_database()
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def list_all_users() -> list:
    db = await get_database()
    users = await db["users"].find({}, {"hashed_password": 0}).to_list(length=None)
    return users


async def update_user_role(user_id: str, role: str) -> dict:
    db = await get_database()
    result = await db["users"].find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": role, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
