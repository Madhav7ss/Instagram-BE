from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    user_name: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=25)

class UserLogin(BaseModel):
    user_name : Optional[str] = Field(None, min_length=3, max_length=20)
    email : Optional[EmailStr] = None
    password: Optional[str] = Field (None, min_length=8 , max_length=25)

class UserUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=100)
    avatar : Optional[str] = None
    
