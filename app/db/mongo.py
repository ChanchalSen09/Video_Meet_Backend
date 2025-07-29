from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from app.core.config import settings

MONGO_CONNECT_TIMEOUT_MS = 5000  # 5 seconds

client = AsyncIOMotorClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=MONGO_CONNECT_TIMEOUT_MS
)

db = client["video_meet"]

async def check_connection() -> bool:
    """
    Ping MongoDB server to check if the connection is alive.
    Returns True if successful, False otherwise.
    """
    try:
        await client.admin.command("ping")
        return True
    except (ServerSelectionTimeoutError, PyMongoError) as e:
        print(f"MongoDB connection error: {e}")
        return False
