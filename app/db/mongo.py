from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

_client: AsyncIOMotorClient | None = None

def connect_to_mongo():
    global _client
    _client = AsyncIOMotorClient(
        settings.MONGO_URI,
        maxPoolSize=10,     # production tuning
        minPoolSize=1
    )

def get_client() -> AsyncIOMotorClient:
    if _client is None:
        raise RuntimeError("MongoDB client not initialized")
    return _client

def close_mongo_connection():
    global _client
    if _client:
        _client.close()