from pydantic import BaseModel


class Like(BaseModel):
    id: str
    entity_id: str
    user_id: str
