from contextlib import asynccontextmanager
from app.db.indexes import create_indexes
from app.db.mongo import connect_to_mongo, close_mongo_connection, get_client
from app.core.config import settings

@asynccontextmanager
async def lifespan(app):
    # 🔹 Startup
    connect_to_mongo()

    client = get_client()
    db = client[settings.MONGO_DB_NAME]

    await create_indexes(db)

    yield

    # 🔹 Shutdown
    close_mongo_connection()