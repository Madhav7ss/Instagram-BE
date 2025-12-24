from fastapi import APIRouter
from app.api.v1 import auth, health,user

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(auth.router, tags=['Auth'])
api_router.include_router(health.router, tags=['Health'])
api_router.include_router(user.router, tags=['User'])