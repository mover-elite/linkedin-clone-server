from pydantic import BaseModel, Field
from app.schemas.common import PyObjectId
import time
from bson import ObjectId
from typing import Optional


class CommentIn(BaseModel):
    post_id: PyObjectId
    content: str


class Comment(CommentIn):
    id: Optional[PyObjectId]
    user_id: PyObjectId
    timestamp: int = Field(default_factory=time.time_ns)


class UserComment(Comment):
    id: PyObjectId = Field(alias="_id")
    user_id: PyObjectId
    user_name: str
    user_username: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
