from pydantic import BaseModel, constr
from typing import List, Optional


class PostModel(BaseModel):
    title: constr(min_length=1, max_length=200)
    body: constr(min_length=1, max_length=2000)
    tags: Optional[List[constr(min_length=1)]] = []
