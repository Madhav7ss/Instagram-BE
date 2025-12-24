from contextlib import asynccontextmanager
from app.db.indexes import create_indexes
from app.db.mongo import db

@asynccontextmanager
async def lifespan(app):
    # Startup
    await create_indexes(db)
    yield
    # Shutdown (optional cleanup)   