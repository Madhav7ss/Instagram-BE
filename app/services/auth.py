from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserLogin
from app.utils.validators.user_validators import username_validator, password_validation
from app.models.user import user_model
from app.utils.password import hash_password, verify_password
from app.core.token import create_access_token
from app.constants.messages import (
    USERNAME_ALREADY_EXISTS,
    EMAIL_ALREADY_USED,
    SOMETHING_WENT_WRONG,
    INVALID_CREDENTIALS,
    EMAIL_USER_REQUIRED
)

class AuthService:

    def __init__(self, db):
        self.db = db
        self.users = db.users

    # ---------------- SIGNUP ----------------

    async def create_user(self, user: UserCreate):
        username_validator(user.user_name)

        if await self.user_name_exists(user.user_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=USERNAME_ALREADY_EXISTS
            )

        password_validation(user.password)
        hashed_password = hash_password(user.password)

        try:
            await self.users.insert_one(
                user_model({
                    "name": user.name,
                    "username": user.user_name,
                    "email": user.email,
                    "password": hashed_password,
                })
            )
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=EMAIL_ALREADY_USED
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=SOMETHING_WENT_WRONG
            )


    async def login(self, user: UserLogin):

        if user.email:
            data = await self.user_by_email(user.email)
        elif user.user_name:
            data = await self.user_by_username(user.user_name)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=EMAIL_USER_REQUIRED
            )

        if not data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS
            )

        if not verify_password(user.password, data["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= INVALID_CREDENTIALS
            )

        token_data = {
            "userId": data["id"],
            "username": data["username"],
            "email": data["email"]
        }

        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def user_name_exists(self, name: str) -> bool:
        return await self.users.find_one({"username": name}) is not None

    async def user_by_username(self, name: str):
        return await self.users.find_one({"username": name})

    async def user_by_email(self, email: str):
        return await self.users.find_one({"email": email})
