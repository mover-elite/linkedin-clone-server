from pydantic import BaseModel


class Post(BaseModel):
    id: str
    user_id: str
    content: str
    timestamp: int
    image_url: str
