from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    post_id: str
    user_id: str
    content: str
    timestamp: int
