from datetime import datetime
from uuid import uuid4

def user_model(user: dict) -> dict:
    return {
        "id" : user.get("id", str(uuid4())),
        # Identity
        "name": user["name"],
        "username": user["username"],   # UNIQUE
        "email": user["email"],          # UNIQUE

        # Security
        "password": user["password"],    # hashed password only

        # References (IDs only)
        "posts": user.get("posts", []),
        "reels": user.get("reels", []),
        "comments": user.get("comments", []),

        # Metadata
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at", datetime.utcnow()),
        "updated_at": user.get("updated_at", datetime.utcnow()),

    }