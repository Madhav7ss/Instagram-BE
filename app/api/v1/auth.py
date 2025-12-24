from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr


router = APIRouter(prefix='/auth')

class User(BaseModel):
    name: str = Field(..., min_length=2)
    user_name: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=25)

@router.post('/signup')
async def create_new_account(user: User):
    pass