from pydantic import BaseModel
from typing import Optional,List

class EmbeddingFace(BaseModel):
    username: Optional[str]
    url: Optional[str]
    embs: List[list]