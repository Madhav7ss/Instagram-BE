from app.db.mongo import db

async def create_indexes(db):
    await db.users.create_index("id", unique=True)
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)