from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import Jwt
from app.crud.user import get_user_by_email
from app.schemas.user import User as UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    payload = await Jwt.decode_access_token(token)
    email = payload["sub"]
    user = await get_user_by_email(email)
    return UserSchema(**user)
