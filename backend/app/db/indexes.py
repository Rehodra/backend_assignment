from app.db.database import get_database


async def create_indexes():
    """Create MongoDB indexes on application startup."""
    try:
        db = await get_database()

        # Unique indexes on users collection
        await db["users"].create_index("email", unique=True)
        await db["users"].create_index("username", unique=True)

        # Indexes for task queries
        await db["tasks"].create_index("owner_id")
        await db["tasks"].create_index("created_at")

        # TTL index on token blacklist
        await db["token_blacklist"].create_index("token", unique=True)
        await db["token_blacklist"].create_index("expires_at", expireAfterSeconds=0)

        print("MongoDB indexes created")
    except Exception as e:
        print(f"Skipping index creation (often unsupported in Mock DB): {e}")

