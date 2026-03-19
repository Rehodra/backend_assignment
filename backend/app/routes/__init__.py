from fastapi import APIRouter
from app.routes import auth, tasks, oauth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(tasks.router)
api_router.include_router(oauth.router)
