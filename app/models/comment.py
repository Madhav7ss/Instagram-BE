from uuid import uuid4
from datetime import datetime
from typing import Optional

def comment_model(data: dict) -> dict:
    return {
        "id": str(uuid4()),
        "post_id": data["post_id"],        # required
        "user_id": data["user_id"],        # from token
        "text": data["text"],              # required

        "parent_id": data.get("parent_id"),  # None = top-level
        "level": data.get("level", 0),        # 0,1,2...

        "reply_count": 0,

        "is_deleted": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
