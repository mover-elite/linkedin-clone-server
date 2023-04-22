from pydantic import BaseModel, Field
from bson import ObjectId
from app.schemas.common import PyObjectId
from typing import Optional


class LoginUser(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "password": "Asfe32A",
            }
        }


class UserIn(LoginUser):
    name: str
    username: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "username": "Doer",
                "email": "jdoe@example.com",
                "password": "Asfe32A",
            }
        }


class User(UserIn):
    id: Optional[PyObjectId] = Field(alias="_id")
    image_url: str = "dunno yet"

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
