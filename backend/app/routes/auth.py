from fastapi import APIRouter, status
from app.schemas.user import (
    UserRegisterRequest, UserLoginRequest,
    RefreshTokenRequest, TokenResponse, UserResponse
)
from app.services import auth_service
from app.core.dependencies import get_current_active_user, require_admin
from fastapi import Depends
from app.schemas.user import UpdateRoleRequest

from app.core.ratelimit import limiter
from fastapi import Request

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="Register a new user")
@limiter.limit("5/minute")
async def register(request: Request, body: UserRegisterRequest):
    user = await auth_service.register_user(
        username=body.username,
        email=body.email,
        password=body.password,
    )
    return _format_user(user)


@router.post("/login", response_model=TokenResponse, summary="Login and get JWT tokens")
@limiter.limit("10/minute")
async def login(request: Request, body: UserLoginRequest):
    return await auth_service.login_user(body.email, body.password)


@router.post("/refresh", response_model=TokenResponse, summary="Refresh access token")
async def refresh(body: RefreshTokenRequest):
    return await auth_service.refresh_access_token(body.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Logout (revoke refresh token)")
async def logout(body: RefreshTokenRequest):
    await auth_service.logout_user(body.refresh_token)


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def me(current_user: dict = Depends(get_current_active_user)):
    return _format_user(current_user)


# ─── Admin only ────────────────────────────────────────────────────────────────

@router.get("/users", summary="[Admin] List all users")
async def list_users(_: dict = Depends(require_admin)):
    users = await auth_service.list_all_users()
    return [_format_user(u) for u in users]


@router.patch("/users/{user_id}/role", response_model=UserResponse, summary="[Admin] Change user role")
async def change_role(user_id: str, body: UpdateRoleRequest, _: dict = Depends(require_admin)):
    user = await auth_service.update_user_role(user_id, body.role)
    return _format_user(user)


def _format_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user.get("is_active", True),
        "created_at": user["created_at"],
    }
