from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.token import verify_access_token
from app.constants.messages import INVALID_TOKEN,AUTHORIZATION_HEADER_MISSING

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= AUTHORIZATION_HEADER_MISSING
        )
    
    # token = credentials.credentials

    # payload = verify_access_token(token)

    # user_id = payload.get("userId")

    # if not user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail= INVALID_TOKEN
    #     )

    return {
        "user_id": 'd3aea2ea-5f41-4863-a03d-97ce49122efd',
        "username": 'Batman'
    }
