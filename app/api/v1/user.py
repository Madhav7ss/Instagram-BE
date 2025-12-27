from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from app.core.dependencies import get_current_user
from app.db.debs import get_db
from app.services.users import UserService
from app.schemas.response import SuccessResponse
from app.constants.messages import FOLLOWING_SUCCESSFULL, UN_FOLLOWING_SUCCESSFULL, USER_RETRIEVED_SUCCESS, USER_UPDATE_SUCCESS
from app.schemas.user import UserUpdate

router = APIRouter(prefix='/user')

@router.get('/', status_code=200)
async def get_user_details(id: Optional[str]=Query(None), current_user= Depends(get_current_user), db = Depends(get_db)):
    service = UserService(db)
    response = await service.get_user(id,current_user)
    return SuccessResponse(message = USER_RETRIEVED_SUCCESS, data=response )

@router.patch('/update', status_code=201)
async def update_user_profile(user_details: UserUpdate, current_user= Depends(get_current_user), db = Depends(get_db)):
    service = UserService(db)
    await service.update_user(user_details, current_user)
    return SuccessResponse(message=USER_UPDATE_SUCCESS)

@router.post('/follow/{id}', status_code=201)
async def follow_account(id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    service = UserService(db)
    response = await service.follow_account(id, current_user)
    return SuccessResponse(message=FOLLOWING_SUCCESSFULL, data=response)

@router.post('/unfollow/{id}', status_code=201)
async def follow_account(id: str, current_user = Depends(get_current_user), db = Depends(get_db)):
    service = UserService(db)
    response = await service.un_follow_account(id, current_user)
    return SuccessResponse(message=UN_FOLLOWING_SUCCESSFULL, data=response)