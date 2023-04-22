from pydantic import BaseModel


class Error(BaseModel):
    path: str
    msg: str


class ValidationError(BaseModel):
    errors: list[Error]
