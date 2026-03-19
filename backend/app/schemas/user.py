from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.user import Role


# ─── Request Schemas ───────────────────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        import re
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[\W_]", v):
             raise ValueError("Password must contain at least one special character")
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UpdateRoleRequest(BaseModel):
    role: Role


# ─── Response Schemas ──────────────────────────────────────────────────────────

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: Role
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
