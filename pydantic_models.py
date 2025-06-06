from typing import List
from pydantic import BaseModel, ConfigDict


class PostOut(BaseModel):
    id: int
    category: str
    word_freq: dict

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel):
    total: int
    posts: List[PostOut]