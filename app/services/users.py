from fastapi import status, HTTPException
from app.schemas.user import UserUpdate
from app.constants.messages import GETTING_FOLLOWING_COUNT_FAILED, SOMETHING_WENT_WRONG, FOLLOW_YOURSELF, NOT_FOLLOWING, ALREDAY_FOLLOWING, USER_NOT_FOUND

class UserService:

    def __init__(self, db):
        self.db =db
        self.users = db.users

    async def get_user(self,id: str, current_user:dict):
        try:
            if id:
                user_id = id
            else:
                user_id = current_user.get('user_id')

            response = await self.users.find_one(
                {"id": user_id},
                {"_id":0,"username": 1, "followings_count": 1, "followers_count": 1, "post": 1, "description": 1, "avatar": 1 }
            )
            if not response:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= USER_NOT_FOUND)
            post_count = len(response.get('post', []))
            return {
                "user_name": response.get('username'),
                "followings_count": response.get('followings_count', 0),
                "followers_count": response.get('followers_count', 0),
                "avatar": response.get('avatar', ''),
                "description": response.get('description', ''),
                "post_count": post_count
            }
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)

    async def update_user(self, user: UserUpdate, current_user:dict):
        try:
            user_id = current_user.get('user_id')
            response = await self.users.update_one(
                {"id": user_id},
                {
                    "$set": {"avatar": user.avatar, "description": user.description}
                }
            )

            if not response:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
            return None
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)

    async def follow_account(self, id: str, current_user:dict):
        try:
            user_id = current_user.get('user_id')
            if user_id == id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=FOLLOW_YOURSELF)
            
            result = await self.users.update_one(
                {"id": user_id, "followings": {"$ne": id}},
                {"$addToSet": {"followings": id}, "$inc": {"followings_count": 1}}
            )

            if result.modified_count == 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ALREDAY_FOLLOWING)

            await self.users.update_one(
                {"id": id, "followers": {"$ne": user_id}},
                {"$addToSet": {"followers": user_id}, "$inc": {"followers_count": 1}}
            )
            count = await self.get_follow_count(user_id)
            return count
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)

    async def un_follow_account(self,id: str, current_user:dict):
        try:
            user_id = current_user.get('user_id')
            result = await self.users.update_one(
                {"id": user_id, "followings": id},
                {"$pull": {"followings": id}, "$inc": {"followings_count": -1}}
            )
            if result.modified_count == 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=NOT_FOLLOWING)
            
            await self.users.update_one(
                {"id": id, "followers": user_id},
                {"$pull": {"followers": user_id}, "$inc": {"followers_count": -1}}
            )
            count = await self.get_follow_count(user_id)
            return count
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=SOMETHING_WENT_WRONG)
    
    async def get_follow_count(self, id: str):
        try:
            response = await self.users.find_one(
                {"id": id},
                {"_id": 0, "followings_count": 1, "followers_count": 1}
            )
            if not response:
                return {
                    "Followers_Count": 0,
                    "Followings_Count": 0
                }

            return {
                "Followers_Count": response.get("followers_count", 0),
                "Followings_Count": response.get("followings_count", 0)
            }
        except Exception:
            print(GETTING_FOLLOWING_COUNT_FAILED)