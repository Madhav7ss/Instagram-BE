from app.schemas.post import PostCreate
from app.core.dependencies import get_current_user
from fastapi import Depends, HTTPException, status
from app.models.post import post_model
from app.constants.messages import SOMETHING_WENT_WRONG

class PostService:

    def __init__(self, db):
        self.post = db.post
        self.users = db.users

    async def create_post(self, post: PostCreate, user = Depends(get_current_user)):

        try:
            user_id = user.user_id
            new_post = {
                "user_id": user_id,
                "caption": post.caption,
                "media": post.media
            }

            response = await self.post.insert_one(post_model(new_post))
            post_id = response['id']

            await self.users.update_one(
                {"id": user_id},
                {"$addToSet": {"posts" : post_id}}
            )
            return response
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)
