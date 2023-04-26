from pydantic import BaseModel, Field
from bson import ObjectId
from app.schemas.common import PyObjectId
from typing import Optional
import time


class PostIn(BaseModel):
    content: str
    image_url: Optional[str] = ""

    class Config:
        schema_extra = {
            "example": {
                "content": "This is an example of a post",
                "image_url": "http://example.com",
            }
        }


class Post(PostIn):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId = Field(alias="userId")
    timestamp: int = Field(default_factory=time.time_ns)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "This is an example of a post",
                "image_url": "http://example.com",
                "id": 232323233,
                "user_id": "dsffdfdff",
                "timestamp": 223434343432,
            }
        }


class UserPosts(PostIn):
    id: PyObjectId = Field(alias="_id")
    user_id: PyObjectId
    user_name: str
    user_username: str
    user_email: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
