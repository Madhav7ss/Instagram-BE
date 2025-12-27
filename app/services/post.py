from app.schemas.post import PostCreate, CommentAdd
from fastapi import HTTPException, status
from app.models.post import post_model
from app.models.comment import comment_model
from app.constants.messages import SOMETHING_WENT_WRONG, POST_NOT_FOUND, GETTING_LIKES_COUNT_FAILED, GETTING_FOLLOWING_COUNT_FAILED
from uuid import uuid4


class PostService:

    def __init__(self, db):
        self.post = db.post
        self.users = db.users
        self.comments = db.comments

    async def create_post(self, post: PostCreate, user: dict):

        try:
            user_id = user.get("user_id")
            post_id = str(uuid4())
            new_post = {
                "id": post_id,
                "user_id": user_id,
                "caption": post.caption,
                "media": [item.model_dump() for item in post.media]
            }

            await self.post.insert_one(post_model(new_post))

            await self.users.update_one(
                {"id": user_id},
                {"$addToSet": {"posts": post_id}}
            )
            return {
                "post_id": post_id
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)

    async def get_post(self, post_id: str, user: dict):
        try:
            post = await self.post.find_one({"id": post_id}, {"_id": 0})
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=POST_NOT_FOUND
                )
            return post
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)

    async def add_comment(self, commentData: CommentAdd, user: dict):
        try:
            user_id = user.get("user_id")
            level = 0
            parent_comment = None
            if commentData.replyToCommentId:
                parent_comment = await self.comments.find_one({"id": commentData.replyToCommentId})
                if parent_comment:
                    level = parent_comment.get("level", 0) + 1

            comment = {
                "post_id": commentData.post_id,
                "user_id": user_id,
                "text": commentData.comment,
                "parent_id": commentData.replyToCommentId,
                "level": level
            }

            await self.comments.insert_one(comment_model(comment))

            await self.update_comment_cout(commentData.post_id)

            if parent_comment:
                await self.update_reply_count(commentData.replyToCommentId)

            return {
                "post_id": commentData.post_id,
                "user_id": user_id,
                "text": commentData.comment,
                "parent_id": commentData.replyToCommentId,
                "level": level
            }
        except Exception as e:
            print(f"Error adding comment: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)

    async def update_comment_cout(self, post_id: str):
       # Increment comment count on the post
        await self.post.update_one(
            {"id": post_id},
            {"$inc": {"comments_count": 1}}
        )

    async def update_reply_count(self, parent_comment_id: str):
        await self.comments.update_one(
            {"id": parent_comment_id},
            {"$inc": {"reply_count": 1}}
        ),

    async def get_comments(self, page: int, limit: int, post_id: str, current_user: dict):
        user_id = current_user.get('user_id')
        skip = (page - 1) * limit

        cursor = (self.comments.find(
            {"post_id": post_id, "parent_id": None},
            {"_id": 0}
        ).sort("created_at", 1).skip(skip).limit(limit))

        comments = await cursor.to_list(length=limit)

        total_comment_count = await self.get_comment_count(post_id)

        return {
            "page": page,
            "total": total_comment_count,
            "comments": comments
        }

    async def get_comment_count(self, post_id: str):
        post = await self.post.find_one({"id": post_id})
        return post.get('comments_count')

    async def get_nested_comments(self, page: int, limit: int, post_id: str, parent_comment_id: str):
        skip = (page - 1) * limit

        cursor = ( self.comments.find(
            {"post_id": post_id, "parent_id": parent_comment_id },
            {"_id": 0}
        ).sort("created_at", 1).skip(skip).limit(limit))

        comments = await cursor.to_list(length = limit)

        return {
            "page": page,
            "comments": comments
        }
    
    async def like_post(self,post_id:str, current_user:dict):
        try:
            user_id = current_user.get('user_id')
            await self.post.update_one(
                {'id': post_id, 'likes': {'$ne': user_id}},
                {'$addToSet': {'likes': user_id}, '$inc': {"likes_count": 1}}
            )
            count = await self.get_likes_count(post_id)
            return {
                "Total_Likes": count
            }
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)
    
    async def unlike_post(self,post_id: str, current_user:dict):
        try:
            user_id = current_user.get('user_id')
            await self.post.update_one(
                {"id": post_id, 'likes': user_id },
                {'$pull': { 'likes': user_id}, "$inc": {'likes_count': -1} }
            )

            count = await self.get_likes_count(post_id)

            return {
                "Total_Likes": count
            }

        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)
        
    async def get_likes_count(self, post_id:str):
        try:
            response = await self.post.find_one({'id': post_id}, {"_id": 0, "likes_count": 1})
            return response['likes_count'] if response else 0
        except Exception:
            print(GETTING_LIKES_COUNT_FAILED)

    async def get_posts(self, page:int, limit:int, current_user: dict):
        try:
            user_id = current_user.get('user_id')
            users = await self.users.find_one(
                {"id": user_id},
                {"_id": 0, "followings": 1}
            )

            followings = users['followings'] if users else []
            user_idss = followings + [user_id]

            skip = (page-1) * limit

            cursor = self.post.find(
                {"user_id": {"$in": user_idss}}
            ).sort("created_at", -1).skip(skip).limit(limit)

            posts = await cursor.to_list(length = limit)
            posts = self.order_posts(posts)
            return posts

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)
        

    def order_posts(self,posts: list):
        for post in posts:
             post["score"] = (
                    post.get("like_count", 0) * 2 +
                    post.get("comment_count", 0) * 3
                )
        posts.sort(key=lambda x: x["score"], reverse=True)
        return posts