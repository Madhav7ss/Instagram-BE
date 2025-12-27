from datetime import datetime
from uuid import uuid4

def user_model(user: dict) -> dict:
    return {
        "id" : user.get("id", str(uuid4())),
        # Identity
        "name": user["name"],
        "username": user["username"],   # UNIQUE
        "email": user["email"],          # UNIQUE
        "description": user.get('description', None),
        "avatar": user.get('avatar', None),

        # Security
        "password": user["password"],    # hashed password only

        # References (IDs only)
        "posts": user.get("posts", []),
        "reels": user.get("reels", []),
        "comments": user.get("comments", []),
        "followers_count": 0,
        "followers": user.get("followers", []),
        "followings_count": 0,
        "followings": user.get("followings", []),

        # Metadata
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at", datetime.utcnow()),
        "updated_at": user.get("updated_at", datetime.utcnow()),

    }