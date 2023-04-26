from pydantic import BaseModel, Field
import time
from bson import ObjectId
from app.schemas.common import PyObjectId
from typing import Optional


class LikeOut(BaseModel):
    entity_id: PyObjectId
    user_id: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Like(LikeOut):
    id: Optional[PyObjectId] = Field(alias="_id")
    timestamp: int = Field(default_factory=time.time_ns)
