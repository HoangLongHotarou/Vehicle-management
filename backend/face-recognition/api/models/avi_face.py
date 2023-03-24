from pydantic import BaseMode
from typing import Optional,List

class EmbeddingFace(BaseMode):
    username: Optional[str]
    embeddings: List[any] = []