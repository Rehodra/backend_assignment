from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings

def hash_password(password: str) -> str:
    """Hash a password using pure bcrypt."""
    params = bcrypt.gensalt(rounds=12)
    # bcrypt requires bytes, not str
    encoded_pw = password.encode('utf-8')
    return bcrypt.hashpw(encoded_pw, params).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash using pure bcrypt."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except ValueError:
        return False

def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "type": "access"}
    if isinstance(subject, dict):
        to_encode.update(subject)
    else:
        to_encode.update({"sub": str(subject)})
        
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str | Any) -> str:
    """Generate a JWT refresh token with a longer lifespan."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {"exp": expire, "type": "refresh"}
    if isinstance(subject, dict):
        to_encode.update(subject)
    else:
        to_encode.update({"sub": str(subject)})
        
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
