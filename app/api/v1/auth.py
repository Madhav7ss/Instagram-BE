from fastapi import APIRouter, Depends
from app.db.debs import get_db

from app.schemas.user import UserCreate, UserLogin
from app.services.auth import AuthService
from app.schemas.response import SuccessResponse
from app.constants.messages import USER_CREATED_SUCCESSFULLY, LOGIN_SUCCESSFULLY

router = APIRouter(prefix='/auth')


@router.post('/signup', status_code=201)
async def create_new_account(user: UserCreate, db = Depends(get_db)):
    service = AuthService(db)
    await service.create_user(user)
    return SuccessResponse(message=USER_CREATED_SUCCESSFULLY)

@router.post('/login', status_code=200)
async def login(user: UserLogin, db = Depends(get_db)):
    service = AuthService(db)
    data = await service.login(user)
    return SuccessResponse(message=LOGIN_SUCCESSFULLY, data=data)

from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.get("/swagger-test")
async def swagger_test(token=Depends(security)):
    return {"ok": True}