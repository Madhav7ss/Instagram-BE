from fastapi import APIRouter, Depends, Query
from app.schemas.post import PostCreate, CommentAdd
from app.services.post import PostService
from app.db.debs import get_db
from app.schemas.response import SuccessResponse
from app.constants.messages import POST_CREATED_SUCCESSFULLY, COMMENT_ADDED_SUCCESSFULLY, POST_FETCH_SUCCESSFULLY, COMMENT_RETRIVED_SUCCESSFULLY
from app.core.dependencies import get_current_user

router = APIRouter(prefix='/post')

@router.post('/', status_code=201)
async def create_post(
    post: PostCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    service = PostService(db)
    response = await service.create_post(post, current_user)
    return SuccessResponse(message=POST_CREATED_SUCCESSFULLY, data=response)

@router.get('/{id}', status_code=200)
async def get_post(id: str, db=Depends(get_db), current_user = Depends(get_current_user)):
    service = PostService(db)
    response = await service.get_post(id, current_user)
    return SuccessResponse(message=POST_FETCH_SUCCESSFULLY, data=response)


@router.post('/comment', status_code=201)
async def add_new_comment(comment: CommentAdd, db=Depends(get_db), current_user = Depends(get_current_user)):
    service = PostService(db)
    response = await service.add_comment(comment, current_user)
    return SuccessResponse(message= COMMENT_ADDED_SUCCESSFULLY, data=response)

@router.get('/comments/{id}', status_code=200)
async def get_comments(id: str, page: int = Query(ge=1), limit: int = Query(25,ge=10, le=100), db=Depends(get_db), current_user = Depends(get_current_user)):
    service = PostService(db)
    response = await service.get_comments(page, limit,id,current_user)
    return SuccessResponse(message=COMMENT_RETRIVED_SUCCESSFULLY, data=response)

@router.get("/nested-comments/{id}", status_code=200)
async def get_nested_comments(id: str, page: int = Query(ge=1), limit: int = Query(25,ge=10, le=100),parent_id:str= Query(), db=Depends(get_db)):
    service = PostService(db)
    response = await service.get_nested_comments(page, limit,id, parent_id)
    return SuccessResponse(message=COMMENT_RETRIVED_SUCCESSFULLY, data=response)        
