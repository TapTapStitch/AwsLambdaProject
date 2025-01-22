from pydantic import BaseModel, Field
from typing import List


class PostModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1, max_length=2000)
    tags: List[str] | None = []
