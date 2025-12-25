from app.db.mongo import get_client
from app.core.config import settings

async def get_db():
    client = get_client()
    db = client[settings.MONGO_DB_NAME]
    yield db