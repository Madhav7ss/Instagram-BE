from fastapi import APIRouter, Depends
from app.schemas.post import PostCreate
from app.services.post import PostService
from app.db.debs import get_db
from app.schemas.response import SuccessResponse
from app.constants.messages import POST_CREATED_SUCCESSFULLY

router = APIRouter(prefix='/post')

@router.post('/', status_code=201)
async def create_post(post: PostCreate, db= Depends(get_db)):
    service = PostService(db)
    response = await service.create_post(post, db)
    return SuccessResponse(message= POST_CREATED_SUCCESSFULLY, data=response)