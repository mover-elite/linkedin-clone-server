from app.schemas.user import User as UserSchema, UserIn as UserInSchema
from app.database.mongodb import database
from app.core.security import hash_password


async def create_user(user: UserInSchema) -> UserSchema:
    user_collection = database.users

    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = UserSchema(**user.__dict__)

    res = await user_collection.insert_one(new_user.dict(exclude_unset=True))
    result = await user_collection.find_one({"_id": res.inserted_id})

    saved_user = UserSchema(**result)
    return saved_user


async def get_user_by_email(email: str):
    user_collection = database.users

    res = await user_collection.find_one({"email": email})
    return res
