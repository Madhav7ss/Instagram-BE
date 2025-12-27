
async def create_indexes(db):
    await db.users.create_index("id", unique=True)
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.post.create_index("id", unique=True)
    await db.users.create_index("followers")
    await db.users.create_index("followings")
    await db.post.create_index(
        [("user_id",1), ("created_at", -1)]
    )