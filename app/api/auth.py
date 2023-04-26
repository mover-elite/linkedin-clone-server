from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user
from app.schemas.user import UserIn as UserInSchema, User as UserSchema, LoginUser
from app.crud.user import create_user, get_user_by_email
from app.core.exceptions import BadRequest
from app.core.security import verify_password
from app.core.security import Jwt

from typing import Annotated

router = APIRouter(prefix="/auth")


@router.post(
    "/sign_up",
    response_description="Create new user",
    response_model=UserSchema,
    tags=["Auth"],
)
async def sign_up(user: UserInSchema = Body(...)):
    created_user = await create_user(user)
    return created_user


@router.post("/login", response_description="Login User", tags=["Auth"])
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(form_data.username)
    user = await get_user_by_email(form_data.username)
    if not user:
        raise BadRequest("User not found")
    password_valid = verify_password(form_data.password, user["password"])

    if not password_valid:
        raise BadRequest("Password is incorrect")

    access_token = await Jwt.get_access_token(user["email"])
    print(access_token)
    return {"access_token": access_token}


@router.get("/user/me", tags=["USER"])
async def get_user(user: UserSchema = Depends(get_current_user)):
    return user
