from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

_client = None

async def connect_to_mongo():
    global _client
    if getattr(settings, "USE_MOCK_DB", True):
        from mongomock_motor import AsyncMongoMockClient
        _client = AsyncMongoMockClient()
        print(f"Connected to In-Memory MOCK MongoDB: {settings.MONGO_DB_NAME}")
    else:
        _client = AsyncIOMotorClient(settings.MONGO_URI)
        await _client.admin.command("ping")
        print(f"Connected to MongoDB: {settings.MONGO_DB_NAME}")

async def close_mongo_connection():
    global _client
    if _client:
        # mongomock-motor clients don't always need exact close(), but we call it if exists
        close_func = getattr(_client, "close", None)
        if callable(close_func):
            close_func()
        print("MongoDB connection closed")

async def get_database() -> AsyncIOMotorDatabase:
    return _client[settings.MONGO_DB_NAME]
