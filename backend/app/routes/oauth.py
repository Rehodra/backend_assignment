from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings
from app.db.database import get_database
from app.core.security import create_access_token, create_refresh_token
from datetime import datetime, timezone
from app.services.auth_service import _issue_tokens

router = APIRouter(prefix="/auth", tags=["OAuth"])

class GoogleLoginRequest(BaseModel):
    credential: str

@router.post("/google", summary="Login with Google")
async def google_login(body: GoogleLoginRequest):
    try:
        # Verify the ID token from Google
        idinfo = id_token.verify_oauth2_token(
            body.credential, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo['email']
        username = idinfo.get('name', email.split('@')[0])
        
        db = await get_database()
        user = await db["users"].find_one({"email": email})

        if not user:
            # First user is still admin even via Google
            is_first_user = await db["users"].count_documents({}) == 0
            role = "admin" if is_first_user else "user"
            
            user_doc = {
                "username": username,
                "email": email,
                "hashed_password": None, # No password for Google users
                "role": role,
                "is_active": True,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
                "auth_provider": "google"
            }
            result = await db["users"].insert_one(user_doc)
            user = user_doc
            user["_id"] = result.inserted_id

        return _issue_tokens(user)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
