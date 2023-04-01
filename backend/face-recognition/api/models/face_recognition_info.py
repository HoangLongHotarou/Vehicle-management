from pydantic import BaseModel
from typing import Optional, List


class FaceRecognitionInfo(BaseModel):
    username: Optional[str]
    hash_username: Optional[str]
    len_embs: Optional[int] = 0
    url: Optional[str]
