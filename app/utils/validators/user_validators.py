import re 
from fastapi import HTTPException, status
from app.constants.patterns import (
    USERNAME_REGEX,
    PASSWORD_UPPERCASE_REGEX,
    PASSWORD_NUMBER_REGEX,
    PASSWORD_SPECIAL_CHAR_REGEX,
)
from app.constants.messages import (
    USERNAME_INVALID_FORMAT,
    PASSWORD_UPPERCASE_REQUIRED,
    PASSWORD_NUMBER_REQUIRED,
    PASSWORD_SPECIAL_CHAR_REQUIRED,
)

def username_validator(username:str):
    if not re.match(USERNAME_REGEX, username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USERNAME_INVALID_FORMAT)
    
def password_validation(password: str):
    if not re.search(PASSWORD_UPPERCASE_REGEX, password):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=PASSWORD_UPPERCASE_REQUIRED)
    if not re.search(PASSWORD_NUMBER_REGEX, password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=PASSWORD_NUMBER_REQUIRED)
    if not re.search(PASSWORD_SPECIAL_CHAR_REGEX, password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=PASSWORD_SPECIAL_CHAR_REQUIRED)