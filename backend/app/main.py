from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import connect_to_mongo, close_mongo_connection
from app.db.indexes import create_indexes
from app.routes import api_router

import logging
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.ratelimit import limiter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to MongoDB and ensure indexes exist
    await connect_to_mongo()
    await create_indexes()
    yield
    # Shutdown: close the connection cleanly
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "A production-ready REST API with JWT authentication, "
        "role-based access control, and task management."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Allow the frontend dev server and any configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/", tags=["Root"], summary="Root")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}. Visit /docs for API documentation."
    }
