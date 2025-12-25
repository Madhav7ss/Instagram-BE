from datetime import datetime
from uuid import uuid4

def post_model(post: dict)-> dict:
    return{
        "id": post.get('id', str(uuid4())),
        "caption": post.get("caption"),
        "user_id": post["user_id"],
        "media":  post["media"],
        "location": post.get("location"),
        "hashtags": post.get("hashtags", []),
        "likes_count": 0,
        "comments_count": 0,
        "is_archived": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }